from appian_locust import AppianTaskSet
from locust import HttpUser, task


class GridTaskSet(AppianTaskSet):

    @task
    def interact_with_grid_in_interface(self):
        # Navigate to the interface backed report that contains a grid
        report_uiform = self.appian.visitor.visit_report(report_name="Employee Report with Grid")

        # Sort the grid rows by the "Department" field name
        report_uiform.sort_paging_grid(label="Employee Directory", field_name="Department", ascending=True)

        # Select the first five rows on the first page of the grid
        report_uiform.select_rows_in_grid(rows=[0, 1, 2, 3, 4], label="Employee Directory")

        # Move to the second page of the grid
        report_uiform.move_to_right_in_paging_grid(label="Employee Directory")

        # Select the first row on the second page of the grid
        report_uiform.select_rows_in_grid(rows=[0], label="Employee Directory", append_to_existing_selected=True)

        # Click on the row with a record link with the given label
        report_uiform.click_record_link(label="William")


class UserActor(HttpUser):
    tasks = [GridTaskSet]
    host = 'https://mysitename.net'
    auth = ["myusername", "mypassword"]

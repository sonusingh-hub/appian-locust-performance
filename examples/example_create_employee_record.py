from appian_locust import AppianTaskSet
from locust import HttpUser, task


class RecordsTaskSet(AppianTaskSet):

    @task
    def create_new_employee(self):
        # Navigate to Employee Record List
        record_list_uiform = self.appian.visitor.visit_record_type(record_type="Employees")

        # Click on "New Employee" Record List Action
        record_list_uiform.click_record_list_action(label="New Employee")

        # Fill in new Employee information
        record_list_uiform.fill_text_field(label="First Name", value="Sample")
        record_list_uiform.fill_text_field(label="Last Name", value="User")
        record_list_uiform.fill_text_field(label="Department", value="Engineering")
        record_list_uiform.fill_text_field(label="Title", value="Senior Software Engineer")
        record_list_uiform.fill_text_field(label="Phone Number", value="(703) 442-8844")

        # Create Employee!
        record_list_uiform.click_button(label="Create")


class UserActor(HttpUser):
    tasks = [RecordsTaskSet]
    host = 'https://mysitename.net'
    auth = ["myusername", "mypassword"]

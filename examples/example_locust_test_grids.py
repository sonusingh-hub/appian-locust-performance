import sys
from appian_locust import AppianTaskSet
from locust import HttpUser, task,between
from appian_locust.utilities.loadDriverUtils import loadDriverUtils
from appian_locust.utilities import logger

# loadDriverUtils looks for a configuration file in your test's directory named 'config.json'.
# You can alter this behavior by passing your configuration file name into load_config. Eg: load_config(config_file='<your-config-file.json>')
utls = loadDriverUtils()
utls.load_config()
CONFIG = utls.c

logger = logger.getLogger(__file__)
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

        # Click on the row with a record link with the given label (Change label name below with the one that presents in UI after above steps)
        report_uiform.click_record_link(label="Paul Martin")

class GridUserActor(HttpUser):
    tasks = [GridTaskSet]

    # These determine how long each user waits between @task runs.
    # A random wait time will be chosen between min_wait and max_wait
    # for each task run, ie this script has no waiting by default.
    wait_time = between(0.500, 0.500)

    host = "https://" + CONFIG['host_address']
    auth = CONFIG["auth"]

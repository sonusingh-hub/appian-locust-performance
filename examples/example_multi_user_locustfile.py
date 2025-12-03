from locust import HttpUser, task, between
from appian_locust import AppianTaskSet
from appian_locust.utilities import loadDriverUtils

# loadDriverUtils looks for a configuration file in your test's directory named 'config.json'.
# You can alter this behavior by passing your configuration file name into load_config. Eg: load_config(config_file='<your-config-file.json>')
# Example config file for this test is in this directory with name 'example_admin_config.json'
utls = loadDriverUtils()
utls.load_config()

class GetFrontPageTaskSet(AppianTaskSet):
    @task
    def browse_records(self):
        # Regular user workflow
        self.appian.visitor.visit_site("support", "tickets")

class GetAdminPageTaskSet(AppianTaskSet):
    @task
    def manager_operations(self):
        # Manager-specific workflow with elevated permissions
        self.appian.visitor.visit_site("manager", "overview")

class FrontendUserActor(HttpUser):
    """
    Regular users that interact with standard interfaces.
    Weight will be relative to all defined weights, 4 in this example.
    In this configuration we expect 3 regular users for every manager user.
    """
    tasks = [GetFrontPageTaskSet]
    host = f'https://{utls.c["host_address"]}'
    auth = utls.c["auth"][1]  # Frontend user auth entry
    wait_time = between(0.5, 1.0)
    weight = 3

class AdminUserActor(HttpUser):
    """
    Manager users with elevated privileges and different workflows.
    Weight will be relative to all defined weights, 4 in this example.
    In this configuration we expect 3 regular users for every manager user.
    """
    tasks = [GetAdminPageTaskSet]
    host = f'https://{utls.c["host_address"]}'
    auth = utls.c["auth"][0]  # Admin user auth entry
    wait_time = between(1.0, 2.0)
    weight = 1

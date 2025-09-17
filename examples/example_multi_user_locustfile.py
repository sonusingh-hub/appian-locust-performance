from locust import HttpUser, task, between
from appian_locust import AppianTaskSet
from appian_locust.utilities import loadDriverUtils

utls = loadDriverUtils()
utls.load_config()

class RegularUserTaskSet(AppianTaskSet):
    @task
    def browse_records(self):
        # Regular user workflow
        self.appian.visitor.visit_site("support", "tickets")

class ManagerUserTaskSet(AppianTaskSet):
    @task
    def manager_operations(self):
        # Manager-specific workflow with elevated permissions
        self.appian.visitor.visit_site("manager", "overview")

class RegularUserActor(HttpUser):
    """
    Regular users that interact with standard interfaces.
    Weight will be relative to all defined weights, 4 in this example.
    In this configuration we expect 3 regular users for every manager user.
    """
    tasks = [RegularUserTaskSet]
    host = f'https://{utls.c["host_address"]}'
    auth = utls.c["auth"][0]  # First auth entry
    wait_time = between(0.5, 1.0)
    weight = 3

class ManagerUserActor(HttpUser):
    """
    Manager users with elevated privileges and different workflows.
    Weight will be relative to all defined weights, 4 in this example.
    In this configuration we expect 3 regular users for every manager user.
    """
    tasks = [ManagerUserTaskSet]
    host = f'https://{utls.c["host_address"]}'
    auth = utls.c["auth"][1]  # Second auth entry
    wait_time = between(1.0, 2.0)
    weight = 1
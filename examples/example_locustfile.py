from locust import HttpUser, task
from appian_locust import AppianTaskSet


class GetReportsTaskSet(AppianTaskSet):

    @task
    def get_all_reports(self):
        self.appian.reports_info.get_all_available_reports()


class UserActor(HttpUser):
    tasks = [GetReportsTaskSet]
    host = 'https://mysitename.net'
    auth = ["myusername", "mypassword"]

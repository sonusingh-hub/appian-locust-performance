from locust import TaskSet, Locust
from requests import Response
from .mock_client import CustomLocust
from .mock_reader import read_mock_file
from appian_locust import AppianTaskSet
from appian_locust._reports import ALL_REPORTS_URI
import unittest
import json


class TestReports(unittest.TestCase):
    reports = read_mock_file("reports_response.json")

    def setUp(self) -> None:
        self.custom_locust = CustomLocust(Locust())
        parent_task_set = TaskSet(self.custom_locust)
        setattr(parent_task_set, "host", "")
        setattr(parent_task_set, "auth", ["fake_user", ""])
        self.task_set = AppianTaskSet(parent_task_set)
        self.task_set.host = ""

        # test_on_start_auth_success is covered here.
        self.custom_locust.set_response("auth?appian_environment=tempo", 200, '{}')
        self.task_set.on_start()

    def tearDown(self) -> None:
        self.task_set.on_stop()

    def test_reports_get_all(self) -> None:
        self.custom_locust.set_response(ALL_REPORTS_URI, 200, self.reports)

        all_reports = self.task_set.appian.metadata_provider.get_all_reports()
        self.assertIsInstance(all_reports, dict)

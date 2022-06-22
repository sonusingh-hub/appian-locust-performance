import unittest

from locust import TaskSet, Locust, stats
from .mock_client import CustomLocust
from .mock_reader import read_mock_file
from appian_locust import AppianTaskSet, SailUiForm, ApplicationUiForm, DesignUiForm, DesignObjectUiForm
from appian_locust.helper import ENV
from appian_locust._reports import REPORTS_INTERFACE_PATH, REPORTS_NAV_PATH


class TestVisitor(unittest.TestCase):
    design_landing_page = read_mock_file("design_landing_page.json")

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

        # Setup responses for page types
        self.setUp_report_responses()

    def setUp_report_responses(self) -> None:
        self.custom_locust.set_response("/suite/rest/a/uicontainer/latest/reports", 200, read_mock_file("reports_response.json"))
        self.custom_locust.set_response(REPORTS_INTERFACE_PATH, 200, read_mock_file("reports_interface.json"))
        self.custom_locust.set_response(REPORTS_NAV_PATH, 200, read_mock_file("reports_nav.json"))

    def tearDown(self) -> None:
        self.task_set.on_stop()

    def test_visit_report_success(self) -> None:
        self.custom_locust.set_response("/suite/rest/a/sites/latest/D6JMim/pages/reports/report/qdjDPA/reportlink",
                                        200, '{"context":123, "uuid":123}')

        sail_form = self.task_set.appian.visitor.visit_report(
            "RTE Basic Test Report", False)
        self.assertTrue(isinstance(sail_form, SailUiForm))

    def test_visit_report_failure(self) -> None:
        self.custom_locust.set_response("/suite/rest/a/sites/latest/D6JMim/pages/reports/report/qdjDPA/reportlink",
                                        200, '{"context":123, "uuid":123}')

        report_name = "Fake Report"
        exact_match = False
        with self.assertRaises(Exception) as context:
            self.task_set.appian.visitor.visit_report(
                report_name, exact_match)
        self.assertEqual(
            context.exception.args[0], f"There is no report with name {report_name} in the system under test (Exact match = {exact_match})")

    def test_design_visit_error(self) -> None:
        ENV.stats.clear_all()
        self.custom_locust.set_response(
            "/suite/rest/a/applications/latest/app/design", 400, "")
        with self.assertRaises(Exception) as context:
            sail_form = self.task_set.appian.visitor.visit_design()
        # Two errors will be logged, one at the get_page request level, and one at the visit
        self.assertEqual(2, len(ENV.stats.errors))

        # Assert error structure
        error: stats.StatsError = list(ENV.stats.errors.values())[1]
        self.assertEqual('DESC: No description', error.method)
        self.assertEqual('LOCATION: _design.py/fetch_design_json()', error.name)
        self.assertEqual('EXCEPTION: 400 Client Error: None for uri: /suite/rest/a/applications/latest/app/design Username: fake_user', error.error)
        self.assertEqual(1, error.occurrences)

    def test_visit_design(self) -> None:
        self.custom_locust.set_response(
            "/suite/rest/a/applications/latest/app/design", 200, self.design_landing_page)
        ENV.stats.clear_all()
        design_form = self.task_set.appian.visitor.visit_design()
        self.assertEqual(type(design_form), DesignUiForm)
        self.assertEqual(0, len(ENV.stats.errors))

    def test_visit_application(self) -> None:
        app_id = "thisIsAnAppId"
        self.custom_locust.set_response(
            f"/suite/rest/a/applications/latest/app/design/app/{ app_id }", 200, read_mock_file("design_app_landing_page.json"))
        ENV.stats.clear_all()
        sail_form = self.task_set.appian.visitor.visit_application(app_id)
        self.assertEqual(type(sail_form), ApplicationUiForm)
        self.assertEqual(0, len(ENV.stats.errors))

    def test_visit_design_object(self) -> None:
        design_object_id = "thisIsADesignObjectId"
        self.custom_locust.set_response(
            f"/suite/rest/a/applications/latest/app/design/{ design_object_id }", 200, self.design_landing_page)
        ENV.stats.clear_all()
        sail_form = self.task_set.appian.visitor.visit_design_object(design_object_id)
        self.assertEqual(type(sail_form), DesignObjectUiForm)
        self.assertEqual(0, len(ENV.stats.errors))


if __name__ == '__main__':
    unittest.main()

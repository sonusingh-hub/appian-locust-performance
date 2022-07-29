import unittest
import json

from typing import Any
from locust import TaskSet, Locust, stats
from .mock_client import CustomLocust
from .mock_reader import read_mock_file
from appian_locust import AppianTaskSet, SailUiForm, ApplicationUiForm, DesignUiForm, DesignObjectUiForm, RecordListUiForm, RecordInstanceUiForm
from appian_locust.helper import ENV
from appian_locust._reports import REPORTS_INTERFACE_PATH, REPORTS_NAV_PATH
from appian_locust._records import RECORDS_INTERFACE_PATH, RECORDS_NAV_PATH


class TestVisitor(unittest.TestCase):
    design_landing_page = read_mock_file("design_landing_page.json")
    record_types = read_mock_file("record_types_response.json")
    # Record Instance List for a specific RecordType
    records = read_mock_file("records_response.json")
    grid_records = read_mock_file("records_grid_response.json")
    # Record Summary dashboard response for a specific Record Instance
    record_summary_view = read_mock_file("record_summary_view_response.json")
    record_instance_name = "Actions Page"
    records_interface = read_mock_file("records_interface.json")
    records_nav = read_mock_file("records_nav.json")

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

        # Set up responses for records
        self.setUp_record_responses()

    def setUp_report_responses(self) -> None:
        self.custom_locust.set_response("/suite/rest/a/uicontainer/latest/reports", 200, read_mock_file("reports_response.json"))
        self.custom_locust.set_response(REPORTS_INTERFACE_PATH, 200, read_mock_file("reports_interface.json"))
        self.custom_locust.set_response(REPORTS_NAV_PATH, 200, read_mock_file("reports_nav.json"))

    def setUp_record_responses(self) -> None:
        self.custom_locust.set_response("/suite/rest/a/applications/latest/app/records/view/all", 200,
                                        self.record_types)
        self.custom_locust.set_response("/suite/rest/a/sites/latest/D6JMim/pages/records/recordType/commit", 200,
                                        self.records)
        self.custom_locust.set_response("/suite/rest/a/applications/latest/legacy/tempo/records/type/commit/view/all", 200,
                                        self.records)
        self.custom_locust.set_response("/suite/rest/a/sites/latest/D6JMim/pages/records/recordType/BE5pSw", 200,
                                        self.grid_records)
        self.custom_locust.set_response("/suite/rest/a/applications/latest/legacy/tempo/records/type/BE5pSw/view/all", 200,
                                        self.grid_records)
        self.custom_locust.set_response(
            "/suite/rest/a/sites/latest/D6JMim/page/records/record/lQB0K7YxC0UQ2Fhx4pmY1F49C_MjItD4hbtRdKDmOo6V3MOBxI47ipGa_bJKZf86CLtvOCp1cfX-sa2O9hp6WTKZpbGo5MxRaaTwMkcYMeDl8kN8Hg/view/summary",
            200,
            self.record_summary_view)
        self.custom_locust.set_response(RECORDS_INTERFACE_PATH, 200, self.records_interface)
        self.custom_locust.set_response(RECORDS_NAV_PATH, 200, self.records_nav)

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

    @unittest.mock.patch('appian_locust.records_helper.find_component_by_attribute_in_dict', return_value={'children': None})
    def test_records_form_no_embedded_summary(self, find_component_by_attribute_in_dict_function: Any) -> None:
        with self.assertRaises(Exception) as context:
            self.task_set.appian.visitor.visit_record_instance(
                record_type="Commits",
                record_name=self.record_instance_name,
                view_url_stub="summary",
                exact_match=False)
        self.assertEqual(
            context.exception.args[0],
            "Parser was not able to find embedded SAIL code within JSON response for the requested Record Instance.")

    def test_record_types_form_example_success(self) -> None:
        sail_form = self.task_set.appian.visitor.visit_record_type(
            "Commits",
            exact_match=False
        )
        self.assertTrue(isinstance(sail_form, RecordListUiForm))

    def test_record_type_random_form_example_success(self) -> None:
        sail_form = self.task_set.appian.visitor.visit_record_type(exact_match=False)
        self.assertTrue(isinstance(sail_form, RecordListUiForm))

    def test_record_type_form_incorrect_type(self) -> None:
        record_type = "Fake Type"
        exact_match = True
        with self.assertRaises(Exception) as context:
            self.task_set.appian.visitor.visit_record_type(
                record_type,
                exact_match
            )
        self.assertEqual(
            context.exception.args[0], f"There is no record type with name {record_type} in the system under test")

    @unittest.mock.patch('appian_locust.records_helper.find_component_by_attribute_in_dict', return_value={'children': [json.dumps({"a": "b"})]})
    def test_records_form_example_success(self, find_component_by_attribute_in_dict_function: Any) -> None:
        sail_form = self.task_set.appian.visitor.visit_record_instance(
            "Commits",
            self.record_instance_name,
            view_url_stub="summary",
            exact_match=False
        )
        self.assertTrue(isinstance(sail_form, RecordInstanceUiForm))
        self.assertEqual(sail_form.get_response(), {"a": "b"})

    def test_records_form_incorrect_name(self) -> None:
        record_name = "Fake Record"
        record_type = "Commits"
        exact_match = False
        self.custom_locust.set_response("/suite/rest/a/sites/latest/D6JMim/pages/records/recordType/commit?searchTerm=Fake%20Record", 200,
                                        self.records)
        self.custom_locust.set_response("/suite/rest/a/sites/latest/D6JMim/pages/records/recordType/BE5pSw?searchTerm=Fake%20Record", 200,
                                        self.grid_records)
        with self.assertRaises(Exception) as context:
            self.task_set.appian.visitor.visit_record_instance(
                record_type,
                record_name,
                view_url_stub="summary",
                exact_match=exact_match
            )
        self.assertEqual(
            context.exception.args[0], f"There is no record with name {record_name} found in record type {record_type} (Exact match = {exact_match})")

    def test_records_form_incorrect_type(self) -> None:
        exact_match = False
        with self.assertRaises(Exception) as context:
            self.task_set.appian.visitor.visit_record_instance(
                "Fake Type",
                self.record_instance_name,
                view_url_stub="summary",
                exact_match=exact_match
            )
        self.assertEqual(
            context.exception.args[0], f"There is no record type with name Fake Type in the system under test (Exact match = {exact_match})")


if __name__ == '__main__':
    unittest.main()

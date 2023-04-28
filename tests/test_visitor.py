import unittest
from unittest.mock import patch, MagicMock
import json

from typing import Any
from locust import TaskSet, Locust, stats
from .mock_client import CustomLocust
from .mock_reader import read_mock_file
from appian_locust import AppianTaskSet, SailUiForm, ApplicationUiForm, DesignUiForm, DesignObjectUiForm, RecordListUiForm, RecordInstanceUiForm
from appian_locust.helper import ENV
from appian_locust._tasks import _Tasks
from appian_locust._reports import REPORTS_INTERFACE_PATH
from appian_locust._records import RECORDS_INTERFACE_PATH
from appian_locust._sites import _Sites
from appian_locust.uiform import (ComponentNotFoundException,
                                  ChoiceNotFoundException, InvalidComponentException)
from appian_locust._actions import ACTIONS_ALL_PATH, ACTIONS_INTERFACE_PATH, ACTIONS_FEED_PATH

class TestVisitor(unittest.TestCase):
    design_landing_page = read_mock_file("design_landing_page.json")
    task_feed_resp = read_mock_file("tasks_response.json")
    task_feed_with_next = read_mock_file("tasks_response_with_next.json")
    record_types = read_mock_file("record_types_response.json")
    # Record Instance List for a specific RecordType
    records = read_mock_file("records_response.json")
    grid_records = read_mock_file("records_grid_response.json")
    # Record Summary dashboard response for a specific Record Instance
    record_summary_view = read_mock_file("record_summary_view_response.json")
    record_instance_name = "Actions Page"
    records_interface = read_mock_file("records_interface.json")
    records_nav = read_mock_file("records_nav.json")
    sites_nav_resp = read_mock_file("sites_nav_resp.json")
    actions = read_mock_file("actions_response.json")
    actions_interface = read_mock_file("actions_interface.json")
    actions_nav = read_mock_file("actions_nav.json")
    actions_feed = read_mock_file("actions_feed.json")

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

        # Setup responses for tasks
        self.setUp_task_responses()

        # Setup responses for page types
        self.setUp_report_responses()

        # Setup responses for records
        self.setUp_record_responses()

        # Setup responses for sites
        self.setUp_sites_responses()

        # Setup responses for actions
        self.setUp_actions_json()

    def setUp_task_responses(self) -> None:
        self.custom_locust.set_response(_Tasks.INITIAL_FEED_URI, 200, self.task_feed_resp)

    def get_task_attributes(self, is_auto_acceptable: bool) -> str:
        return f"""
        {{
            "isOfflineTask": false,
            "isSailTask": true,
            "isQuickTask": false,
            "taskId": "1",
            "isAutoAcceptable": {'true' if is_auto_acceptable else 'false'}
        }}"""

    def setUp_report_responses(self) -> None:
        self.custom_locust.set_response("/suite/rest/a/uicontainer/latest/reports", 200, read_mock_file("reports_response.json"))
        self.custom_locust.set_response(REPORTS_INTERFACE_PATH, 200, read_mock_file("reports_interface.json"))
        self.custom_locust.set_response("/suite/rest/a/sites/latest/D6JMim/page/reports/nav", 200, read_mock_file("reports_nav.json"))

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
        self.custom_locust.set_response("/suite/rest/a/sites/latest/D6JMim/page/records/nav", 200, self.records_nav)

    def setUp_sites_responses(self) -> None:
        page_resp_json = read_mock_file("page_resp.json")
        all_sites_str = read_mock_file("all_sites.json")
        self.custom_locust.set_response("/suite/rest/a/sites/latest/D6JMim/page/news/nav", 200, all_sites_str)
        self.custom_locust.client.set_default_response(200, page_resp_json)

    def setUp_sites_json(self, site_name: str) -> None:
        self.custom_locust.set_response(f"/suite/rest/a/sites/latest/{site_name}/nav", 200, self.sites_nav_resp)

    def setUp_actions_json(self) -> None:
        self.custom_locust.set_response(
            "auth?appian_environment=tempo", 200, '{}')
        self.custom_locust.set_response(
            "/suite/api/tempo/open-a-case/available-actions?ids=%5B%5D", 200, self.actions)
        self.custom_locust.set_response(ACTIONS_INTERFACE_PATH, 200, self.actions_interface)
        self.custom_locust.set_response("/suite/rest/a/sites/latest/D6JMim/page/actions/nav", 200, self.actions_nav)
        self.custom_locust.set_response(ACTIONS_FEED_PATH, 200, self.actions_feed)

    def tearDown(self) -> None:
        self.task_set.on_stop()

    def test_visit_task_success(self) -> None:
        task_to_accept = read_mock_file('task_accept_resp.json')
        self.custom_locust.set_response(
            "/suite/rest/a/task/latest/1/status",
            200,
            task_to_accept
        )
        self.custom_locust.set_response(
            "/suite/rest/a/task/latest/1/form",
            200,
            task_to_accept
        )
        self.custom_locust.set_response(
            "/suite/rest/a/task/latest/1/attributes",
            200,
            self.get_task_attributes(is_auto_acceptable=False))
        output = self.task_set.appian.visitor.visit_task("t-1", False)
        self.assertEqual(output.form_url, "/suite/rest/a/task/latest/1/form")

    def test_visit_task_failure(self) -> None:
        task_to_accept = read_mock_file('task_accept_resp.json')
        self.custom_locust.set_response(
            "/suite/rest/a/task/latest/1/status",
            200,
            task_to_accept
        )
        self.custom_locust.set_response(
            "/suite/rest/a/task/latest/1/form",
            200,
            task_to_accept
        )
        self.custom_locust.set_response(
            "/suite/rest/a/task/latest/1/attributes",
            200,
            self.get_task_attributes(is_auto_acceptable=False))

        task_name = "nonexistent task"
        exact_match = False
        with self.assertRaises(Exception) as context:
            self.task_set.appian.visitor.visit_task(task_name, exact_match)
            self.assertEqual(context.exception.args[0], f"There is no task with name {task_name} in the system under test (Exact match = {exact_match})")

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
        self.assertEqual(sail_form.get_latest_state(), {"a": "b"})

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

    def test_visit_site_recordlist_and_get_random_record_form_failure(self) -> None:
        site_name = "abc"
        page_name = "create-mrn"
        link_type = "report"  # Default Page Info

        self.setUp_sites_json(site_name)
        expected_uuid = 'abc123'
        expected_context = '{"abc":"123"}'
        expected_url = f"/suite/rest/a/sites/latest/{site_name}/pages/{page_name}/{link_type}"
        form_content = f'{{"context":{expected_context}, "uuid":"{expected_uuid}", "links":[{{"href": "{expected_url}", "rel": "update"}}]}}'
        self.custom_locust.set_response(expected_url,
                                        200,
                                        form_content)
        with self.assertRaises(Exception) as context:
            self.task_set.appian.visitor.visit_site_recordlist_and_get_random_record_form(site_name, page_name)
        self.assertEqual(
            context.exception.args[0], f"Page {page_name} on site {site_name} is not of type record")

    def test_visit_site_recordlist_failure(self) -> None:
        site_name = "abc"
        page_name = "create-mrn"
        link_type = "report"  # Default Page Info

        self.setUp_sites_json(site_name)
        expected_uuid = 'abc123'
        expected_context = '{"abc":"123"}'
        expected_url = f"/suite/rest/a/sites/latest/{site_name}/pages/{page_name}/{link_type}"
        form_content = f'{{"context":{expected_context}, "uuid":"{expected_uuid}", "links":[{{"href": "{expected_url}", "rel": "update"}}]}}'
        self.custom_locust.set_response(expected_url,
                                        200,
                                        form_content)
        with self.assertRaises(Exception) as context:
            self.task_set.appian.visitor.visit_site_recordlist(site_name, page_name)
        self.assertEqual(
            context.exception.args[0], f"Page {page_name} on site {site_name} is not of type record")

    def test_visit_site(self) -> None:
        site_name = "abc"
        page_name = "create-mrn"
        link_type = "report"  # Default Page Info

        self.setUp_sites_json(site_name)
        expected_uuid = 'abc123'
        expected_context = '{"abc":"123"}'
        expected_url = f"/suite/rest/a/sites/latest/{site_name}/pages/{page_name}/{link_type}"
        form_content = f'{{"context":{expected_context}, "uuid":"{expected_uuid}", "links":[{{"href": "{expected_url}", "rel": "update"}}]}}'
        self.custom_locust.set_response(expected_url,
                                        200,
                                        form_content)
        ui_form: SailUiForm = self.task_set.appian.visitor.visit_site(site_name, page_name)
        self.assertEqual(expected_uuid, ui_form.uuid)
        self.assertEqual(json.loads(expected_context), ui_form.context)
        self.assertEqual(expected_url, ui_form.form_url)

    def setup_action_response_no_ui(self) -> None:
        action = self.task_set.appian.tempo_navigator.navigate_to_actions_and_get_info().get_action_info("Create a Case", False)
        self.custom_locust.set_response(action['formHref'], 200, "{}")

    def setup_action_response_with_ui(self, file_name: str = "form_content_response.json") -> None:
        action = self.task_set.appian.tempo_navigator.navigate_to_actions_and_get_info().get_action_info("Create a Case", False)
        resp_json = read_mock_file(file_name)
        self.custom_locust.set_response(action['formHref'], 200, resp_json)

    def test_actions_visit(self) -> None:
        self.setup_action_response_no_ui()
        action = self.task_set.appian.visitor.visit_action("Create a Case", False).get_latest_state()
        self.assertIsInstance(action, dict)

    def test_actions_form_example_success(self) -> None:
        # output of get_page of a form (SAIL)
        self.setup_action_response_with_ui()
        self.custom_locust.set_response('/suite/rest/a/model/latest/228/form',
                                        200,
                                        '{"context": "12345","links": [{"href": "https://instance.host.net/suite/form","rel": "update","title": "Update", \
                                        "type": "application/vnd.appian.tv.ui+json; c=2; t=START_FORM","method": "POST"}], "ui": {"#t": "UiComponentsDelta","modifiedComponents": []}}')
        sail_form: SailUiForm = self.task_set.appian.visitor.visit_action(
            "Create a Case", False)

        label = 'Title'
        value = "Look at me, I am filling out a form"
        button_label = 'Submit'
        latest_form = sail_form.fill_text_field(label, value).click(button_label)

        resp = latest_form.get_latest_state()
        self.assertEqual("12345", resp['context'])

    def test_actions_form_example_activity_chained(self) -> None:
        action = self.task_set.appian.tempo_navigator.navigate_to_actions_and_get_info().get_action_info("Create a Case", False)
        resp_json = read_mock_file("form_content_response.json")

        self.custom_locust.set_response(action['formHref'], 200, '{"mobileEnabled": "false", "empty": "true", "formType": "START_FORM"}')
        self.custom_locust.set_response(action['initiateActionHref'], 200, resp_json)
        self.custom_locust.set_response(
            '/suite/rest/a/model/latest/228/form',
            200,
            '{"context": "12345","links": [{"href": "https://instance.host.net/suite/form","rel": "update","title": "Update", \
            "type": "application/vnd.appian.tv.ui+json; c=2; t=START_FORM","method": "POST"}], "ui": {"#t": "UiComponentsDelta","modifiedComponents": []}}')
        sail_form: SailUiForm = self.task_set.appian.visitor.visit_action("Create a Case")

        label = 'Title'
        value = "Look at me, I am filling out a form"
        button_label = 'Submit'
        latest_form = sail_form.fill_text_field(label, value).click(button_label)

        resp = latest_form.get_latest_state()
        self.assertEqual("12345", resp['context'])

    def test_actions_form_example_missing_field(self) -> None:
        self.setup_action_response_with_ui()
        sail_form: SailUiForm = self.task_set.appian.visitor.visit_action(
            "Create a Case", False)

        value = "Look at me, I am filling out a form"
        label = "missingText"
        with self.assertRaises(ComponentNotFoundException) as context:
            sail_form.fill_text_field(label, value)
        self.assertEqual(
            context.exception.args[0], f"No components with label 'missingText' found on page")

        button_label = 'press me'
        with self.assertRaises(ComponentNotFoundException) as context:
            sail_form.click(button_label)
        self.assertEqual(
            context.exception.args[0], f"No components with label '{button_label}' found on page")

    def test_actions_form_example_bad_response(self) -> None:
        self.setup_action_response_with_ui()
        sail_form: SailUiForm = self.task_set.appian.visitor.visit_action(
            "Create a Case", False)

        self.custom_locust.set_response(
            '/suite/rest/a/model/latest/228/form', 200, 'null')

        value = "Look at me, I am filling out a form"
        label = "Title"
        with self.assertRaises(Exception) as context:
            sail_form.fill_text_field(label, value)
        self.assertEqual(
            context.exception.args[0], f"No response returned when trying to update the field with 'label' = 'Title' at index '1'")

        button_label = 'Submit'
        with self.assertRaises(Exception) as context:
            sail_form.click(button_label)
        self.assertEqual(
            context.exception.args[0], f"No response returned when trying to click button with label '{button_label}'")

    def test_actions_form_dropdown_errors(self) -> None:
        self.setup_action_response_with_ui('dropdown_test_ui.json')

        sail_form: SailUiForm = self.task_set.appian.visitor.visit_action(
            "Create a Case", False)

        dropdown_label = "missing dropdown"
        with self.assertRaises(ComponentNotFoundException) as context:
            sail_form.select_dropdown_item(dropdown_label, 'some choice')
        self.assertEqual(
            context.exception.args[0], f"No components with label '{dropdown_label}' found on page")

        dropdown_label = "Name"
        with self.assertRaises(InvalidComponentException):
            sail_form.select_dropdown_item(dropdown_label, 'some choice')

        dropdown_label = "Customer Type"
        with self.assertRaises(ChoiceNotFoundException):
            sail_form.select_dropdown_item(dropdown_label, 'some missing choice')

    @patch('appian_locust.SailUiForm._get_update_url_for_reeval', return_value="/mocked/re-eval/url")
    @patch('appian_locust.uiform._Interactor.send_dropdown_update')
    def test_actions_form_dropdown_success(self, mock_send_dropdown_update: MagicMock,
                                           mock_get_update_url_for_reeval: MagicMock) -> None:
        self.setup_action_response_with_ui('dropdown_test_ui.json')

        sail_form: SailUiForm = self.task_set.appian.visitor.visit_action(
            "Create a Case", False)
        initial_state = sail_form.get_latest_state()

        dropdown_label = "Customer Type"
        sail_form.select_dropdown_item(dropdown_label, 'Buy Side Asset Manager')

        mock_get_update_url_for_reeval.assert_called_with(sail_form.get_latest_state())
        mock_send_dropdown_update.assert_called_once()
        args, kwargs = mock_send_dropdown_update.call_args
        self.assertEqual(args[0], "/mocked/re-eval/url")
        self.assertIsNone(kwargs["url_stub"])
        self.assertNotEqual(sail_form.get_latest_state(), initial_state)

    @patch('appian_locust.SailUiForm._get_update_url_for_reeval', return_value="/mocked/re-eval/url")
    @patch('appian_locust.uiform._Interactor.send_dropdown_update')
    def test_actions_form_record_list_dropdown_success(self, mock_send_dropdown_update: MagicMock,
                                                       mock_get_update_url_for_reeval: MagicMock) -> None:
        # 'dropdown_test_record_list_ui.json' contains a 'sail-application-url' field
        self.setup_action_response_with_ui('dropdown_test_record_list_ui.json')

        sail_form: SailUiForm = self.task_set.appian.visitor.visit_action(
            "Create a Case", False)
        initial_state = sail_form.get_latest_state()

        dropdown_label = "Customer Type"
        sail_form.select_dropdown_item(dropdown_label, 'Buy Side Asset Manager')

        mock_get_update_url_for_reeval.assert_called_with(sail_form.get_latest_state())
        mock_send_dropdown_update.assert_called_once()
        args, kwargs = mock_send_dropdown_update.call_args
        self.assertEqual(args[0], "/mocked/re-eval/url")
        self.assertEqual(kwargs["url_stub"], "url_stub123")
        self.assertNotEqual(sail_form.get_latest_state(), initial_state)

    @patch('appian_locust.uiform._Interactor.send_multiple_dropdown_update')
    def test_multiple_dropdown_not_found(self, mock_send_multiple_dropdown_update: MagicMock) -> None:
        self.setup_action_response_with_ui('dropdown_test_ui.json')
        sail_form: SailUiForm = self.task_set.appian.visitor.visit_action(
            "Create a Case", False)

        dropdown_label = "Regions wrong label"
        with self.assertRaises(ComponentNotFoundException) as context:
            sail_form.select_multi_dropdown_item(dropdown_label, ["Asia"])
        self.assertEqual(
            context.exception.args[0], f"No components with label '{dropdown_label}' found on page")

        dropdown_label = "Regions"
        sail_form.select_multi_dropdown_item(dropdown_label, ["Asia"])
        mock_send_multiple_dropdown_update.assert_called_once()
        args, kwargs = mock_send_multiple_dropdown_update.call_args

    @patch('appian_locust.uiform.find_component_by_attribute_in_dict')
    @patch('appian_locust.uiform._Interactor.select_radio_button')
    def test_actions_form_radio_button_by_label_success(self, mock_select_radio_button: MagicMock,
                                                        mock_find_component_by_label: MagicMock) -> None:
        self.setup_action_response_with_ui('dropdown_test_ui.json')

        sail_form: SailUiForm = self.task_set.appian.visitor.visit_action(
            "Create a Case", False)
        state1 = sail_form.get_latest_state()

        button_label = "test-radio-button"
        sail_form.select_radio_button_by_test_label(button_label, 1)

        button_label = "Qualified Institutional Buyer"
        sail_form.select_radio_button_by_label(button_label, 1)

        args, kwargs = mock_find_component_by_label.call_args_list[0]
        self.assertEqual('testLabel', args[0])

        args_next_call, kwargs_next_call = mock_find_component_by_label.call_args_list[1]
        self.assertEqual('label', args_next_call[0])
        self.assertEqual(2, len(mock_select_radio_button.call_args_list))

    def test_actions_form_radio_button_by_label_error(self) -> None:
        self.setup_action_response_with_ui('dropdown_test_ui.json')

        sail_form: SailUiForm = self.task_set.appian.visitor.visit_action(
            "Create a Case", False)

        button_label = "missing button"
        with self.assertRaises(ComponentNotFoundException) as context:
            sail_form.select_radio_button_by_test_label(button_label, 1)
        self.assertEqual(
            context.exception.args[0], f"No components with testLabel '{button_label}' found on page")

        with self.assertRaises(ComponentNotFoundException) as context:
            sail_form.select_radio_button_by_label(button_label, 1)
        self.assertEqual(
            context.exception.args[0], f"No components with label '{button_label}' found on page")

    @patch('appian_locust.uiform.find_component_by_index_in_dict')
    @patch('appian_locust.uiform._Interactor.select_radio_button')
    def test_actions_form_radio_button_by_index_success(self, mock_select_radio_button: MagicMock,
                                                        mock_find_component_by_index: MagicMock) -> None:
        self.setup_action_response_with_ui('dropdown_test_ui.json')
        sail_form: SailUiForm = self.task_set.appian.visitor.visit_action(
            "Create a Case", False)
        initial_state = sail_form.get_latest_state()
        button_index = 1
        sail_form.select_radio_button_by_index(button_index, 1)

        mock_select_radio_button.assert_called_once()
        mock_find_component_by_index.assert_called_with('RadioButtonField', button_index, initial_state)
        self.assertNotEqual(sail_form.get_latest_state(), initial_state)

    def test_actions_form_radio_button_by_index_error(self) -> None:
        self.setup_action_response_with_ui('dropdown_test_ui.json')

        sail_form: SailUiForm = self.task_set.appian.visitor.visit_action(
            "Create a Case", False)

        index_too_low = -1
        with self.assertRaises(Exception) as context:
            sail_form.select_radio_button_by_index(index_too_low, 1)
        self.assertEqual(
            context.exception.args[0], f"Invalid index: '{index_too_low}'. Please enter a positive number")

        index_too_high = 4
        with self.assertRaises(Exception) as context:
            sail_form.select_radio_button_by_index(index_too_high, 1)
        self.assertEqual(
            context.exception.args[0],
            f"Index: '{index_too_high}' out of range"
        )

        index_invalid = "bad index"
        with self.assertRaises(Exception) as context:
            sail_form.select_radio_button_by_index(index_invalid, 1)
        self.assertEqual(
            context.exception.args[0], f"'<' not supported between instances of 'str' and 'int'")


if __name__ == '__main__':
    unittest.main()

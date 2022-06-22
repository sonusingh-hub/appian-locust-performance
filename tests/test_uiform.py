import datetime
import json
import unittest
from typing import Any, List, Optional
from unittest.mock import MagicMock, call, patch

from appian_locust import AppianTaskSet, SailUiForm
from appian_locust.helper import (ENV, find_component_by_attribute_in_dict,
                                  find_component_by_index_in_dict,
                                  find_component_by_label_and_type_dict)
from appian_locust.uiform import (PROCESS_TASK_LINK_TYPE,
                                  ComponentNotFoundException,
                                  InvalidComponentException)
from locust import TaskSet, User
from requests.exceptions import HTTPError

from .mock_client import CustomLocust
from .mock_reader import read_mock_file
from appian_locust._reports import REPORTS_INTERFACE_PATH, REPORTS_NAV_PATH


class TestSailUiForm(unittest.TestCase):
    reports = read_mock_file("reports_response.json")
    record_instance_response = read_mock_file("record_summary_dashboard_response.json")
    related_action_response = read_mock_file("related_action_response.json")
    spl_response = read_mock_file("test_response.json")
    sites_task_report_resp = read_mock_file("sites_task_report.json")
    date_response = read_mock_file("date_task.json")
    multi_dropdown_response = read_mock_file("dropdown_test_ui.json")
    sail_ui_actions_response = read_mock_file("sail_ui_actions_cmf.json")
    file_upload_initial = read_mock_file("multiple_file_upload_widget.json")
    radio_button_initial = read_mock_file("radio_button_selector.json")
    record_action_launch_form_before_refresh = read_mock_file("record_action_launch_form_before_refresh.json")
    record_action_refresh_response = read_mock_file("record_action_refresh_response.json")
    site_with_record_search_button = read_mock_file("site_with_record_search_button.json")
    uiform_click_record_search_button_response = read_mock_file("uiform_click_record_search_button_response.json")
    design_uri = "/suite/rest/a/applications/latest/app/design"
    report_link_uri = "/suite/rest/a/sites/latest/D6JMim/pages/reports/report/nXLBqg/reportlink"
    date_task_uri = '/suite/rest/a/task/latest/EMlJYSQyFKe2tvm5/form'
    sites_task_uri = '/suite/rest/a/sites/latest/tst-site/pages/action/action'
    multi_dropdown_uri = "/suite/rest/a/sites/latest/io/page/onboarding-requests/action/34"
    report_name = "Batch Query Report"
    picker_label = '1. Select a Customer'
    picker_value = 'Antilles Transport'
    process_model_form_uri = "/suite/rest/a/model/latest/8/form"
    locust_label = "I am a label"
    reports_interface = read_mock_file("reports_interface.json")
    reports_nav = read_mock_file("reports_nav.json")

    def setUp(self) -> None:
        self.custom_locust = CustomLocust(User(ENV))
        parent_task_set = TaskSet(self.custom_locust)
        setattr(parent_task_set, "host", "")
        setattr(parent_task_set, "auth", ["", ""])
        self.task_set = AppianTaskSet(parent_task_set)
        self.task_set.host = ""

        # test_on_start_auth_success is covered here.
        self.custom_locust.set_response("auth?appian_environment=tempo", 200, '{}')
        self.task_set.on_start()

        self.custom_locust.set_response("/suite/rest/a/uicontainer/latest/reports", 200, self.reports)
        ENV.stats.clear_all()
        self.custom_locust.set_response(REPORTS_INTERFACE_PATH, 200, self.reports_interface)
        self.custom_locust.set_response(REPORTS_NAV_PATH, 200, self.reports_nav)

    def test_reports_form_example_fail(self) -> None:
        self.custom_locust.set_response(self.report_link_uri,
                                        500, '{}')
        with self.assertRaises(HTTPError):
            self.task_set.appian.visitor.visit_report(self.report_name, False)

    def test_reports_form_modify_grid(self) -> None:
        form_label = 'Top Sales Reps by Total Sales'
        report_form = read_mock_file("report_with_rep_sales_grid.json")
        self.custom_locust.set_response(self.report_link_uri,
                                        200, report_form)
        sail_form = self.task_set.appian.visitor.visit_report(self.report_name, False)
        self.custom_locust.set_response("/suite/rest/a/sites/latest/D6JMim/pages/reports/report/yS9bXA/reportlink",
                                        200, report_form)

        keyWords: List[dict] = [{'label': form_label}, {'index': 0}]
        for i in range(len(keyWords)):
            keyword_args: dict = keyWords[i]
            sail_form.move_to_beginning_of_paging_grid(**keyword_args)
            sail_form.move_to_end_of_paging_grid(**keyword_args)
            sail_form.move_to_left_in_paging_grid(**keyword_args)
            sail_form.move_to_right_in_paging_grid(**keyword_args)
            keyword_args['field_name'] = 'Total'
            sail_form.sort_paging_grid(**keyword_args)

    def test_reports_form_modify_grid_errors(self) -> None:
        report_form = read_mock_file("report_with_rep_sales_grid.json")
        self.custom_locust.set_response(self.report_link_uri,
                                        200, report_form)
        sail_form = self.task_set.appian.visitor.visit_report(self.report_name, False)
        with self.assertRaisesRegex(Exception, "Grid with label 'dummy_label' not found in form") as context:
            sail_form.move_to_beginning_of_paging_grid(label='dummy_label')
        with self.assertRaisesRegex(Exception, "Index 5 out of range"):
            sail_form.move_to_left_in_paging_grid(index=5)
        with self.assertRaisesRegex(Exception, "Cannot sort, field 'Abc' not found"):
            sail_form.sort_paging_grid(index=0, field_name='Abc')
        with self.assertRaisesRegex(Exception, "Field to sort cannot be blank"):
            sail_form.sort_paging_grid(index=0)
        self.assertEqual(4, len(ENV.stats.errors))

    def test_paging_grid_sort_by_label_finds_grid(self) -> None:
        report_form = read_mock_file("paging_grid_sortable.json")
        self.custom_locust.set_response(self.report_link_uri, 200, report_form)
        sail_form = self.task_set.appian.visitor.visit_report(self.report_name, False)
        self.custom_locust.set_response("/suite/rest/a/sites/latest/D6JMim/pages/reports/report/TNCDrA/reportlink", 200, report_form)
        sail_form.sort_paging_grid(label=" Dogs", field_name="Name")

    def test_datatype_caching(self) -> None:
        body_with_types = read_mock_file("page_resp.json")
        self.custom_locust.set_response(self.report_link_uri,
                                        200, body_with_types)
        self.task_set.appian.visitor.visit_report(self.report_name, False)
        self.assertEqual(len(self.task_set.appian.interactor.datatype_cache._cached_datatype), 105)

        self.task_set.appian.visitor.visit_report(self.report_name, False)
        self.assertEqual(len(self.task_set.appian.interactor.datatype_cache._cached_datatype), 105)

    def test_deployments_click_tab(self) -> None:
        design_landing_page_response = read_mock_file("design_landing_page.json")
        deployment_tab_response = read_mock_file("design_deployments_ui.json")
        deployment_outgoing_tab_response = read_mock_file("design_deployments_outgoing_tab.json")

        self.custom_locust.set_response(self.design_uri,
                                        200, design_landing_page_response)
        design_sail_form = self.task_set.appian.design.visit()

        self.custom_locust.set_response(self.design_uri,
                                        200, deployment_tab_response)
        deployments_sail_form = design_sail_form.click("Deployments")

        self.custom_locust.set_response("/suite/rest/a/applications/latest/app/design/deployments",
                                        200, deployment_outgoing_tab_response)
        outgoing_tab_form = deployments_sail_form.get_latest_form().click_tab_by_label("Outgoing", "deployment-secondary-tabs")

        component = find_component_by_attribute_in_dict("label", "OneApp", outgoing_tab_form.latest_state)
        self.assertEqual("OneApp", component.get('label'))

    def test_deployments_click_tab_exception(self) -> None:
        deployment_tab_response = read_mock_file("design_deployments_ui.json")
        design_landing_page_response = read_mock_file("design_landing_page.json")
        self.custom_locust.set_response(self.design_uri,
                                        200, design_landing_page_response)
        design_sail_form = self.task_set.appian.design.visit()

        self.custom_locust.set_response(self.design_uri,
                                        200, deployment_tab_response)
        deployments_sail_form = design_sail_form.click("Deployments")
        with self.assertRaisesRegex(Exception, "Cannot click a tab with label: 'DoesNotExistLabel' inside the TabButtonGroup component"):
            deployments_sail_form.get_latest_form().click_tab_by_label("DoesNotExistLabel", "deployment-secondary-tabs")

    def test_fill_text_field(self) -> None:
        report_body = read_mock_file("text_fields_same_label.json")
        self.custom_locust.set_response(path=self.report_link_uri, status_code=200, body=report_body)
        sail_form = self.task_set.appian.visitor.visit_report(report_name=self.report_name, exact_match=False)

        label = 'Text'
        value = 'Filling out the form...'
        sail_form.fill_text_field(label, value)

    def test_fill_text_field_by_index(self) -> None:
        report_body = read_mock_file("text_fields_same_label.json")
        self.custom_locust.set_response(path=self.report_link_uri, status_code=200, body=report_body)
        sail_form = self.task_set.appian.visitor.visit_report(report_name=self.report_name, exact_match=False)

        label = 'Text'
        value = 'Filling out the form...'
        index = 1
        sail_form.fill_text_field(label, value, index=index)

    def test_fill_text_field_no_fields(self) -> None:
        report_body = read_mock_file("text_fields_same_label.json")
        self.custom_locust.set_response(path=self.report_link_uri, status_code=200, body=report_body)
        sail_form = self.task_set.appian.visitor.visit_report(self.report_name, exact_match=False)

        label = 'Non-existant label'
        value = 'Filling out the form...'
        with self.assertRaises(ComponentNotFoundException) as context:
            sail_form.fill_text_field(label, value)
        self.assertEqual(
            context.exception.args[0], f"No components with label 'Non-existant label' found on page")

    def test_fill_text_field_out_of_bounds_index(self) -> None:
        report_body = read_mock_file("text_fields_same_label.json")
        self.custom_locust.set_response(path=self.report_link_uri, status_code=200, body=report_body)
        sail_form = self.task_set.appian.visitor.visit_report(self.report_name, exact_match=False)

        label = 'Text'
        value = 'Filling out the form...'
        index = 3
        with self.assertRaisesRegex(Exception, "Index: '3' out of range"):
            sail_form.fill_text_field(label, value, index=index)

    def test_fill_text_field_zero_index(self) -> None:
        report_body = read_mock_file("text_fields_same_label.json")
        self.custom_locust.set_response(path=self.report_link_uri, status_code=200, body=report_body)
        sail_form = self.task_set.appian.visitor.visit_report(self.report_name, exact_match=False)

        label = 'Text'
        value = 'Filling out the form...'
        index = 0
        with self.assertRaisesRegex(Exception, "Invalid index: '0'. Please enter a positive number. Indexing is 1-based to match SAIL indexing convention"):
            sail_form.fill_text_field(label, value, index=index)

    def test_fill_text_field_negative_index(self) -> None:
        report_body = read_mock_file("text_fields_same_label.json")
        self.custom_locust.set_response(path=self.report_link_uri, status_code=200, body=report_body)
        sail_form = self.task_set.appian.visitor.visit_report(self.report_name, exact_match=False)

        label = 'Text'
        value = 'Filling out the form...'
        index = -1
        with self.assertRaisesRegex(Exception, "Invalid index: '-1'. Please enter a positive number"):
            sail_form.fill_text_field(label, value, index=index)

    def test_fill_picker_field_interaction(self) -> None:
        sail_ui_actions_cmf = json.loads(self.sail_ui_actions_response)
        picker_widget_suggestions = read_mock_file("picker_widget_suggestions.json")
        picker_widget_selected = read_mock_file("picker_widget_selected.json")

        self.custom_locust.enqueue_response(200, picker_widget_suggestions)
        self.custom_locust.enqueue_response(200, picker_widget_selected)

        sail_form = SailUiForm(self.task_set.appian.interactor, sail_ui_actions_cmf, self.process_model_form_uri)

        label = self.picker_label
        value = self.picker_value
        sail_form.fill_picker_field(label, value)

    def test_fill_picker_field_user(self) -> None:
        sail_ui_actions_cmf = json.loads(self.sail_ui_actions_response)
        picker_widget_selected = read_mock_file("picker_widget_selected.json")
        label = '1. Select a Customer'
        resp = {
            'testLabel': f'test-{label}',
            '#t': 'PickerWidget',
            'suggestions': [{'identifier': {'id': 1, "#t": "User"}}],
            'saveInto': {},
            '_cId': "abc"
        }
        self.custom_locust.enqueue_response(200, json.dumps(resp))
        self.custom_locust.enqueue_response(200, picker_widget_selected)
        sail_form = SailUiForm(self.task_set.appian.interactor, sail_ui_actions_cmf, self.process_model_form_uri)

        value = 'Admin User'
        sail_form.fill_picker_field(label, value)

    def test_fill_picker_field_suggestions_identifier_is_code(self) -> None:
        sail_ui_actions_cmf = json.loads(self.sail_ui_actions_response)
        picker_widget_suggestions = read_mock_file("picker_widget_suggestions_code.json")
        picker_widget_selected = read_mock_file("picker_widget_selected.json")

        self.custom_locust.enqueue_response(200, picker_widget_suggestions)
        self.custom_locust.enqueue_response(200, picker_widget_selected)
        sail_form = SailUiForm(self.task_set.appian.interactor, sail_ui_actions_cmf, self.process_model_form_uri)

        label = self.picker_label
        value = 'GAC Guyana'

        sail_form.fill_picker_field(label, value, identifier='code')

    def test_fill_picker_field_no_suggestions(self) -> None:
        sail_ui_actions_cmf = json.loads(self.sail_ui_actions_response)
        picker_widget_suggestions = read_mock_file("picker_widget_no_suggestions.json")

        self.custom_locust.enqueue_response(200, picker_widget_suggestions)
        sail_form = SailUiForm(self.task_set.appian.interactor, sail_ui_actions_cmf, self.process_model_form_uri)

        label = self.picker_label
        value = 'You will not find me'
        with self.assertRaises(ComponentNotFoundException) as context:
            sail_form.fill_picker_field(label, value)
        self.assertEqual(context.exception.args[0], "No components with type 'PickerWidget' found on page")

    def test_fill_picker_field_no_response(self) -> None:
        sail_ui_actions_cmf = json.loads(self.sail_ui_actions_response)
        self.custom_locust.enqueue_response(200, '{}')
        sail_form = SailUiForm(self.task_set.appian.interactor, sail_ui_actions_cmf, self.process_model_form_uri)

        label = self.picker_label
        value = 'You will not find me'
        with self.assertRaisesRegex(Exception, "No response returned"):
            sail_form.fill_picker_field(label, value)

    def test_fill_picker_field_no_identifiers(self) -> None:
        sail_ui_actions_cmf = json.loads(self.sail_ui_actions_response)
        label = self.picker_label
        resp = {
            'testLabel': f'test-{label}',
            '#t': 'PickerWidget',
            'suggestions': [{'a': 'b'}]
        }
        self.custom_locust.enqueue_response(200, json.dumps(resp))
        sail_form = SailUiForm(self.task_set.appian.interactor, sail_ui_actions_cmf, self.process_model_form_uri)

        value = self.picker_value
        with self.assertRaisesRegex(Exception, "No identifiers found"):
            sail_form.fill_picker_field(label, value)

    def test_fill_picker_field_not_id_or_v(self) -> None:
        sail_ui_actions_cmf = json.loads(self.sail_ui_actions_response)
        label = self.picker_label
        resp = {
            'testLabel': f'test-{label}',
            '#t': 'PickerWidget',
            'suggestions': [{'identifier': {'idx': 1}}]
        }
        self.custom_locust.enqueue_response(200, json.dumps(resp))
        sail_form = SailUiForm(self.task_set.appian.interactor, sail_ui_actions_cmf, self.process_model_form_uri)

        value = self.picker_value
        with self.assertRaisesRegex(Exception, "Could not extract picker values"):
            sail_form.fill_picker_field(label, value)

    def test_fill_picker_field_interaction_no_selection_resp(self) -> None:
        sail_ui_actions_cmf = json.loads(self.sail_ui_actions_response)
        picker_widget_suggestions = read_mock_file("picker_widget_suggestions.json")

        self.custom_locust.enqueue_response(200, picker_widget_suggestions)
        self.custom_locust.enqueue_response(200, '{}')

        sail_form = SailUiForm(self.task_set.appian.interactor, sail_ui_actions_cmf, self.process_model_form_uri)

        label = self.picker_label
        value = self.picker_value
        with self.assertRaisesRegex(Exception, 'No response returned'):
            sail_form.fill_picker_field(label, value)

    def test_upload_document_invalid_component(self) -> None:
        with self.assertRaisesRegex(Exception, 'Provided component was not a FileUploadWidget'):
            label = 'my_label'
            ui = {
                'contents': [

                    {
                        "contents": {
                            "label": label,
                            "#t": "Some other thing"
                        },
                        "label": label,
                        "labelPosition": "ABOVE",
                        "instructions": "",
                        "instructionsPosition": "",
                        "helpTooltip": "Upload an application or a multi-patch package",
                        "requiredStyle": "",
                        "skinName": "",
                        "marginBelow": "",
                        "accessibilityText": "",
                        "#t": "FieldLayout"
                    },
                ]
            }
            sail_form = SailUiForm(self.task_set.appian.interactor, ui, self.process_model_form_uri)
            sail_form.upload_document_to_upload_field(label, 'fake_file')

    def test_upload_document_missing_file(self) -> None:
        file = 'fake_file'
        with self.assertRaisesRegex(Exception, f"No such file or directory: '{file}'"):
            label = 'my_label'
            ui = {
                'contents': [

                    {
                        "label": label,
                        "labelPosition": "ABOVE",
                        "instructions": "",
                        "instructionsPosition": "",
                        "helpTooltip": "Upload an application or a multi-patch package",
                        "requiredStyle": "",
                        "skinName": "",
                        "marginBelow": "",
                        "accessibilityText": "",
                        "#t": "FileUploadWidget"
                    },
                ]
            }
            sail_form = SailUiForm(self.task_set.appian.interactor, ui, self.process_model_form_uri)
            sail_form.upload_document_to_upload_field(label, file)

    def test_multi_upload_document_invalid_component(self) -> None:
        with self.assertRaisesRegex(Exception, 'Provided component was not a MultipleFileUploadWidget'):
            label = 'Form'
            ui = ui = {
                'contents': [

                    {
                        "label": label,
                        "labelPosition": "ABOVE",
                        "instructions": "",
                        "instructionsPosition": "",
                        "helpTooltip": "Upload an application or a multi-patch package",
                        "requiredStyle": "",
                        "skinName": "",
                        "marginBelow": "",
                        "accessibilityText": "",
                        "#t": "FormLayout"
                    },
                ]
            }
            sail_form = SailUiForm(self.task_set.appian.interactor, ui, self.process_model_form_uri)
            sail_form.upload_documents_to_multiple_file_upload_field(label, 'fake_file')

    def test_multi_upload_document_invalid_file(self) -> None:
        with self.assertRaisesRegex(FileNotFoundError, "No such file or directory: "):
            ui = json.loads(self.file_upload_initial)
            label = 'File Upload 5'
            sail_form = SailUiForm(self.task_set.appian.interactor, ui, self.process_model_form_uri)
            sail_form.upload_documents_to_multiple_file_upload_field(label, ['fake_file'])

    @patch('appian_locust.SailUiForm.upload_documents_to_multiple_file_upload_field')
    def test_single_to_multi_upload_document(self, mock_upload_documents_to_multiple_file_upload_field: MagicMock) -> None:
        ui = json.loads(self.file_upload_initial)
        label = 'File Upload 5'
        sail_form = SailUiForm(self.task_set.appian.interactor, ui, self.process_model_form_uri)
        sail_form.upload_document_to_upload_field(label, 'fake_file')
        mock_upload_documents_to_multiple_file_upload_field.assert_called_once()
        args, kwargs = mock_upload_documents_to_multiple_file_upload_field.call_args_list[0]
        self.assertEqual(args[1], ['fake_file'])

    @patch('os.path.exists', return_value=True)
    @patch('appian_locust.uiform._Interactor.upload_document_to_field')
    @patch('appian_locust.uiform._Interactor.upload_document_to_server')
    def test_single_to_multi_upload_document_to_server(self, mock_upload_document_to_server: MagicMock,
                                                       mock_upload_document_to_field: MagicMock,
                                                       mock_os_path_exists: MagicMock) -> None:
        ui = json.loads(self.file_upload_initial)
        label = 'File Upload 5'
        sail_form = SailUiForm(self.task_set.appian.interactor, ui, self.process_model_form_uri)

        sail_form.upload_document_to_upload_field(label, 'fake_file')

        mock_upload_document_to_server.assert_called_once_with('fake_file', is_encrypted=False)
        mock_upload_document_to_field.assert_called_once()

    @patch('appian_locust.SailUiForm.upload_document_to_upload_field')
    def test_multi_to_single_upload_document(self, mock_upload_document_to_upload_field: MagicMock) -> None:
        ui = json.loads(self.file_upload_initial)
        label = 'File Upload 4'
        sail_form = SailUiForm(self.task_set.appian.interactor, ui, self.process_model_form_uri)
        sail_form.upload_documents_to_multiple_file_upload_field(label, 'fake_file')
        mock_upload_document_to_upload_field.assert_called_once()

    def test_click_related_action_on_record_form(self) -> None:
        self.custom_locust.set_response('/suite/rest/a/record/latest/BE5pSw/ioBHer_bdD8Emw8hMSiA_CnpxaK0CVK61sPetEqM0lI_pHvjAsXVOlJtUo/actions/'
                                        'ioBHer_bdD8Emw8hMSiA_CnpxaA0SVKp1kzE9BURlYvkxHjzPlX0d81Hmk',
                                        200,
                                        self.related_action_response)
        sail_form = SailUiForm(self.task_set.appian.interactor,
                               json.loads(self.record_instance_response),
                               '/suite/rest/a/sites/latest/D6JMim/page/records/record/'
                               'lIBHer_bdD8Emw8hLPETeiApJ24AA5ZJilzpBmewf--PdHDSUx022ZVdk6bhtcs5w_3twr_z1drDBwn8DKfhPp90o_A4GrZbDSh09DYkh5Mfq48'
                               '/view/summary')
        record_instance_header_form = sail_form.get_record_header_form()
        # perform a related action
        record_instance_related_action_form = record_instance_header_form.click_related_action("Discuss Case History")

        # Assert fields on the related action form
        text_component = find_component_by_attribute_in_dict('label', 'Action Type', record_instance_related_action_form.state)
        self.assertEqual(text_component.get("#t"), "TextField")

    def test_click_related_action_link_on_summary_dashboard(self) -> None:
        related_action_dialog_response = read_mock_file("related_action_in_a_dialog_response.json")
        record_instance_with_related_action_link_response = read_mock_file("record_summary_with_related_action_response.json")

        # Mocking the response for related action
        self.custom_locust.set_response('/suite/rest/a/record/latest/lMBIWonPMarTw_zHV5oHY7Qv6e46NZWjhAVMg-o7QVtt-3W0zJoYQxILKZhEkSJs0tCAhEektXxP2N01AkR32ISfkpTKGeoz4L6tNR8PBwsRRWEtw/'
                                        'actionDialog/iwBIWonPMarTw_zHTsSC5HBmvtUFIZ8Nar8xAVLL-EvREVFV-D4OAWQ4z8a2Q',
                                        200, related_action_dialog_response)

        sail_form = SailUiForm(self.task_set.appian.interactor,
                               json.loads(record_instance_with_related_action_link_response),
                               'suite/rest/a/sites/latest/connected-servicing/page/servicing-requests/record/'
                               'lMBIWonPMarTw_zHV9tHY7Qv243EjNNOfm68ODkwcOZV5QkPIy_jUPbUMBdKMU5co2siOSdlQZiECCP4MTqB25k7gOVE83gI-zLH97k_QuvUtK0sQ/view/summary'
                               )
        record_summary_view_form = sail_form.get_record_view_form()
        # perform a related action that opens in a dialog (which is a on the summary dashboard itself)
        record_instance_related_action_form = record_summary_view_form.click_related_action("Document Reconciliation")

        # Assert fields on the related action form
        dropdown_component = find_component_by_attribute_in_dict('label', 'Document Type', record_instance_related_action_form.state)
        self.assertEqual(dropdown_component.get("#t"), "DropdownField")

    @patch('appian_locust._interactor._Interactor.get_page')
    def test_filter_records_using_searchbox(self, mock_get_page: MagicMock) -> None:
        uri = 'suite/rest/a/sites/latest/D6JMim/pages/records/recordType/commit'
        record_type_list_form = SailUiForm(self.task_set.appian.interactor,
                                           json.loads(read_mock_file("records_response.json")),
                                           uri)
        record_type_list_form.filter_records_using_searchbox("Actions Page")

        mock_get_page.assert_called_once()
        args, kwargs = mock_get_page.call_args_list[0]
        self.assertEqual(kwargs['uri'], f"{uri}?searchTerm=Actions%20Page")
        self.assertEqual(kwargs['headers']['Accept'], "application/vnd.appian.tv.ui+json")

    @patch('appian_locust._interactor._Interactor.click_start_process_link')
    def test_click_start_process_link(self, mock_click_spl: MagicMock) -> None:
        uri = self.report_link_uri
        test_form = SailUiForm(self.task_set.appian.interactor, json.loads(self.spl_response), uri)
        mock_component_object = {
            "processModelOpaqueId": "iQB8GmxIr5iZT6YnVytCx9QKdJBPaRDdv_-hRj3HM747ZtRjSw",
            "cacheKey": "c93e2f33-06eb-42b2-9cfc-2c4a0e14088e"
        }
        test_form._click_start_process_link("z1ck30E1", "home", False, component=mock_component_object,
                                            locust_request_label="I am a label!")

        mock_click_spl.assert_called_once()
        args, kwargs = mock_click_spl.call_args_list[0]

        self.assertEqual(kwargs['component'], mock_component_object)
        self.assertEqual(kwargs['process_model_opaque_id'], "iQB8GmxIr5iZT6YnVytCx9QKdJBPaRDdv_-hRj3HM747ZtRjSw")
        self.assertEqual(kwargs['cache_key'], "c93e2f33-06eb-42b2-9cfc-2c4a0e14088e")
        self.assertEqual(kwargs['is_mobile'], False)
        self.assertEqual(kwargs['locust_request_label'], "I am a label!")

    @patch('appian_locust.uiform.SailUiForm._click_start_process_link')
    def test_click_card_layout_by_index_spl(self, mock_click_spl: MagicMock) -> None:
        uri = self.report_link_uri
        test_form = SailUiForm(self.task_set.appian.interactor,
                               json.loads(self.spl_response),
                               uri)
        component = find_component_by_label_and_type_dict('label', 'Request Pass', 'StartProcessLink', test_form.state)
        test_form.click_card_layout_by_index(1, locust_request_label=self.locust_label)

        mock_click_spl.assert_called_once()
        args, kwargs = mock_click_spl.call_args_list[0]

        self.assertTupleEqual(args, ('z1ck30E1', 'home', False, component))
        self.assertEqual(kwargs["locust_request_label"], self.locust_label)

    @patch('appian_locust._interactor._Interactor.click_component')
    def test_click_card_layout_by_index_other_link(self, mock_click_component: MagicMock) -> None:
        uri = self.report_link_uri
        test_form = SailUiForm(self.task_set.appian.interactor,
                               json.loads(self.spl_response),
                               uri)

        def get_call(name: str) -> Optional[Any]:
            return {
                'uuid': test_form.uuid,
                'context': test_form.context
            }.get(name)

        mock_state = MagicMock()
        mock_state.get.side_effect = get_call
        mock_click_component.return_value = mock_state
        component = find_component_by_index_in_dict("DynamicLink", 3, test_form.state)
        test_form.click_card_layout_by_index(3, locust_request_label=self.locust_label)

        mock_click_component.assert_called_once()
        args, kwargs = mock_click_component.call_args_list[0]
        self.assertEqual(args[0], self.report_link_uri)
        self.assertEqual(args[1], component)
        self.assertEqual(args[2], test_form.context)
        self.assertEqual(args[3], test_form.uuid)
        self.assertEqual(kwargs["label"], self.locust_label)

    @patch('appian_locust._interactor._Interactor.select_radio_button')
    def test_radio_button_select_by_label(self, mock_radio_select_component: MagicMock) -> None:
        uri = self.report_link_uri
        test_form = SailUiForm(self.task_set.appian.interactor,
                               json.loads(self.radio_button_initial),
                               uri)
        component = find_component_by_attribute_in_dict("label", "Cool Buttons", test_form.state)
        test_uuid = test_form.uuid
        test_context = test_form.context
        test_form.select_radio_button_by_label("Cool Buttons", 1, locust_request_label=self.locust_label)
        mock_radio_select_component.assert_called_once()
        args, kwargs = mock_radio_select_component.call_args_list[0]
        self.assertEqual(args[0], self.report_link_uri)
        self.assertEqual(args[1], component)
        self.assertEqual(args[2], test_context)
        self.assertEqual(args[3], test_uuid)
        self.assertEqual(kwargs["context_label"], self.locust_label)

    def test_click_card_layout_by_index_no_link(self) -> None:
        uri = self.report_link_uri
        test_form = SailUiForm(self.task_set.appian.interactor,
                               json.loads(self.spl_response),
                               uri)

        with self.assertRaisesRegex(Exception, "CardLayout found at index: 2 does not have a link on it"):
            test_form.click_card_layout_by_index(2)

    def _setup_date_form(self) -> SailUiForm:
        uri = self.date_task_uri
        self.custom_locust.set_response(self.date_task_uri, 200, self.date_response)
        test_form = SailUiForm(self.task_set.appian.interactor,
                               json.loads(self.date_response),
                               uri)
        return test_form

    def _setup_multi_dropdown_form(self) -> SailUiForm:
        uri = self.multi_dropdown_uri
        self.custom_locust.set_response(self.multi_dropdown_uri, 200, self.multi_dropdown_response)
        test_form = SailUiForm(self.task_set.appian.interactor,
                               json.loads(self.multi_dropdown_response),
                               uri)
        return test_form

    def _setup_action_response_with_ui(self, file_name: str = "form_content_response.json") -> None:
        action = self.task_set.appian.actions.get_action("Create a Case", False)
        resp_json = read_mock_file(file_name)
        self.custom_locust.set_response(action['formHref'], 200, resp_json)

    def test_reconcile_ui_changes_context(self) -> None:
        # State one
        test_form = self._setup_date_form()
        original_uuid = test_form.uuid
        original_context = test_form.context
        # State two, different uuid
        new_state = json.loads(self.spl_response)

        test_form._reconcile_state(new_state)

        self.assertNotEqual(test_form.uuid, original_uuid)
        self.assertNotEqual(test_form.context, original_context)
        self.assertEqual(test_form.uuid, new_state['uuid'])
        self.assertEqual(test_form.context, new_state['context'])

    def _unwrap_value(self, json_str: str) -> str:
        return json.loads(json_str)['updates']['#v'][0]['value']['#v']

    def test_fill_datefield_not_found(self) -> None:
        test_form = self._setup_date_form()
        with self.assertRaises(ComponentNotFoundException) as context:
            test_form.fill_date_field('Datey', datetime.date.today())
        self.assertEqual(context.exception.args[0], "No components with label 'Datey' found on page")

    def test_fill_datefield_bad_input(self) -> None:
        test_form = self._setup_date_form()
        with self.assertRaisesRegex(Exception, "Input must be of type date"):
            test_form.fill_date_field('Dt', 'abc')

    def test_fill_datefield_success(self) -> None:
        test_form = self._setup_date_form()
        test_form.fill_date_field('Date', datetime.date(1990, 1, 5))

        last_request = self.custom_locust.get_request_list().pop()
        self.assertEqual('post', last_request['method'])
        self.assertEqual(self.date_task_uri, last_request['path'])
        self.assertEqual('1990-01-05Z', self._unwrap_value(last_request['data']))

    def test_get_dropdown_choices_multiple(self) -> None:
        resp_json = read_mock_file(file_name='dropdown_test_ui.json')
        ui_form = SailUiForm(self.task_set.appian.interactor, json.loads(resp_json), '')
        choices = ui_form.get_dropdown_items("Customer Type")
        self.assertEqual(["-- Please select a value --",
                          "Buy Side Asset Manager",
                          "Corporate Banking",
                          "Institutional Investor",
                          "Sell Side ",
                          "SME Banking"], choices)

    def test_get_dropdown_choices_errors(self) -> None:
        resp_json = read_mock_file(file_name='dropdown_test_ui.json')
        ui_form = SailUiForm(self.task_set.appian.interactor, json.loads(resp_json), '')
        with self.assertRaises(ComponentNotFoundException):
            ui_form.get_dropdown_items("Dropdown that DNE")
        with self.assertRaises(InvalidComponentException):
            ui_form.get_dropdown_items("Domicile")

    def test_empty_get_dropdown_choices(self) -> None:
        state = {'ui': [{'label': "Empty Dropdown", 'choices': []}]}
        ui_form = SailUiForm(self.task_set.appian.interactor, state, '')
        self.assertEqual([], ui_form.get_dropdown_items("Empty Dropdown"))

    def test_select_multi_dropdown_success(self) -> None:
        test_form = self._setup_multi_dropdown_form()
        test_form.select_multi_dropdown_item('Regions', ["Asia", "Africa and Middle East"])
        last_request = self.custom_locust.get_request_list().pop()
        self.assertEqual('post', last_request['method'])
        self.assertEqual(self.multi_dropdown_uri, last_request['path'])
        self.assertEqual([1, 2], self._unwrap_value(last_request["data"]))

    def test_fill_datetimefield_bad_input(self) -> None:
        test_form = self._setup_date_form()
        with self.assertRaisesRegex(Exception, "Input must be of type datetime"):
            test_form.fill_datetime_field('Dt', 'abc')

    def test_fill_datetimefield_not_found(self) -> None:
        test_form = self._setup_date_form()
        with self.assertRaises(ComponentNotFoundException) as context:
            test_form.fill_datetime_field('Dt', datetime.datetime.now())
        self.assertEqual(context.exception.args[0], "No components with label 'Dt' found on page")

    def test_fill_datetimefield_success(self) -> None:
        test_form = self._setup_date_form()
        test_form.fill_datetime_field('Date Time', datetime.datetime(1990, 1, 2, 1, 30, 50))

        last_request = self.custom_locust.get_request_list().pop()
        self.assertEqual('post', last_request['method'])
        self.assertEqual(self.date_task_uri, last_request['path'])
        self.assertEqual('1990-01-02T01:30:00Z', self._unwrap_value(last_request['data']))

    def _setup_grid_form(self) -> SailUiForm:
        uri = self.sites_task_uri
        self.custom_locust.set_response(uri, 200, self.sites_task_report_resp)
        test_form = SailUiForm(self.task_set.appian.interactor,
                               json.loads(self.sites_task_report_resp),
                               uri)
        return test_form

    def test_select_grid_row_success(self) -> None:
        test_form = self._setup_grid_form()
        test_form.select_rows_in_grid([2], "My Tasks")

        last_request = self.custom_locust.get_request_list().pop()
        self.assertEqual('post', last_request['method'])
        self.assertEqual(self.sites_task_uri, last_request['path'])

        update = json.loads(last_request['data'])['updates']['#v'][0]['value']
        self.assertEqual("GridSelection", update['#t'])
        selected_list = update['selected']
        self.assertEqual(1, len(selected_list))
        selected = selected_list[0]
        self.assertEqual("int", selected['#t'])
        self.assertEqual(268435892, selected['#v'])

    def test_multi_select_grid_row_success(self) -> None:
        test_form = self._setup_grid_form()
        test_form.select_rows_in_grid([0, 2], "My Tasks")

        last_request = self.custom_locust.get_request_list().pop()
        self.assertEqual('post', last_request['method'])
        self.assertEqual(self.sites_task_uri, last_request['path'])

        update = json.loads(last_request['data'])['updates']['#v'][0]['value']
        self.assertEqual("GridSelection", update['#t'])
        selected_list = update['selected']
        self.assertEqual(2, len(selected_list))

        first_selected = selected_list[0]
        self.assertEqual("int", first_selected['#t'])
        self.assertEqual(536871411, first_selected['#v'])

        second_selected = selected_list[1]
        self.assertEqual("int", second_selected['#t'])
        self.assertEqual(268435892, second_selected['#v'])

    def test_dispatch_click_task_no_id(self) -> None:
        uri = self.report_link_uri
        sites_task_report = SailUiForm(self.task_set.appian.interactor,
                                       json.loads(self.sites_task_report_resp),
                                       uri)
        component = {'#t': PROCESS_TASK_LINK_TYPE, 'label': "my task"}
        with self.assertRaisesRegex(Exception, "No task id found for task with name 'my task'"):
            sites_task_report._dispatch_click(component, 'no label')

    def test_dispatch_click_task_with_id(self) -> None:
        uri = self.report_link_uri
        sites_task_report = SailUiForm(self.task_set.appian.interactor,
                                       json.loads(self.sites_task_report_resp),
                                       uri)
        initial_uuid = sites_task_report.uuid
        initial_context = sites_task_report.context
        task_to_accept = read_mock_file('task_accept_resp.json')
        self.custom_locust.set_response(
            "/suite/rest/a/task/latest/Bs3k2OfS55jCOcMb5D/status",
            200,
            task_to_accept
        )
        self.custom_locust.set_response(
            "/suite/rest/a/task/latest/Bs3k2OfS55jCOcMb5D/attributes",
            200,
            """{
            "isOfflineTask": false,
            "isSailTask": true,
            "isQuickTask": false,
            "taskId": "Bs3k2OfS55jCOcMb5D",
            "isAutoAcceptable": "true"
            }""")
        sites_task_report.click('Issue recommendation')

        task_to_accept_state = json.loads(task_to_accept)

        self.assertNotEqual(initial_uuid, sites_task_report.uuid)
        self.assertNotEqual(initial_context, sites_task_report.context)
        self.assertEqual(task_to_accept_state['uuid'], sites_task_report.uuid)
        self.assertEqual(task_to_accept_state['context'], sites_task_report.context)

        # Assert ui state updated
        self.assertEqual('Available Case Workers',
                         find_component_by_attribute_in_dict('label', 'Available Case Workers', sites_task_report.state).get('label')
                         )

    def test_refresh_after_record_action_interaction(self) -> None:
        sail_ui_record_action_before = json.loads(self.record_action_launch_form_before_refresh)

        self.custom_locust.enqueue_response(200, self.record_action_refresh_response)

        sail_form = SailUiForm(self.task_set.appian.interactor, sail_ui_record_action_before, "http://localhost.com")

        sail_form.refresh_after_record_action("Update Table 1 (Dup) (PSF)")

    def test_click_record_search_button_by_index(self) -> None:
        sail_ui_site_with_record_search_button = json.loads(self.site_with_record_search_button)

        self.custom_locust.enqueue_response(200, self.uiform_click_record_search_button_response)

        sail_form = SailUiForm(self.task_set.appian.interactor, sail_ui_site_with_record_search_button, "http://localhost.com")

        sail_form.click_record_search_button_by_index()

    @patch('appian_locust._interactor._Interactor.click_record_link')
    def test_click_record_link(self, mock_click_rl: MagicMock) -> None:
        report_body = read_mock_file("nested_dynamic_link_response.json")
        self.custom_locust.set_response(path=self.report_link_uri, status_code=200, body=report_body)
        sail_form = self.task_set.appian.visitor.visit_report(self.report_name, exact_match=False)

        sail_form.click_record_link('')

        args, _ = mock_click_rl.call_args_list[0]

        self.assertEqual(args[1]['recordIdentifier'], '74')

    @patch('appian_locust._interactor._Interactor.click_record_link')
    def test_click_record_view_link(self, mock_click_rl: MagicMock) -> None:
        report_body = read_mock_file("nested_dynamic_link_response.json")
        self.custom_locust.set_response(path=self.report_link_uri, status_code=200, body=report_body)
        sail_form = self.task_set.appian.visitor.visit_report(self.report_name, exact_match=False)

        sail_form.click_record_view_link(label='Related Actions')

        args, _ = mock_click_rl.call_args_list[0]

        print(f"args: {args[1]}")

        self.assertEqual(args[1]['recordIdentifier'], '101')

    @patch('appian_locust._interactor._Interactor.click_record_link')
    def test_click_record_link_by_index(self, mock_click_rl: MagicMock) -> None:
        report_body = read_mock_file("nested_dynamic_link_response.json")
        self.custom_locust.set_response(path=self.report_link_uri, status_code=200, body=report_body)
        sail_form = self.task_set.appian.visitor.visit_report(self.report_name, exact_match=False)

        sail_form.click_record_link_by_index(index=2)

        args, _ = mock_click_rl.call_args_list[0]

        self.assertEqual(args[1]['recordIdentifier'], '22')

    @patch('appian_locust._interactor._Interactor.click_record_link')
    def test_click_record_link_by_attribute_and_index(self, mock_click_rl: MagicMock) -> None:
        report_body = read_mock_file("nested_dynamic_link_response.json")
        self.custom_locust.set_response(path=self.report_link_uri, status_code=200, body=report_body)
        sail_form = self.task_set.appian.visitor.visit_report(self.report_name, exact_match=False)

        sail_form.click_record_link_by_attribute_and_index(attribute='pageUrlStub', attribute_value='reports', index=3)

        args, _ = mock_click_rl.call_args_list[0]

        self.assertEqual(args[1]['recordIdentifier'], '112')

    def test_click_record_link_missing_attribute(self) -> None:
        report_body = read_mock_file("nested_dynamic_link_response.json")
        self.custom_locust.set_response(path=self.report_link_uri, status_code=200, body=report_body)
        sail_form = self.task_set.appian.visitor.visit_report(self.report_name, exact_match=False)

        with self.assertRaises(ComponentNotFoundException) as context:
            sail_form.click_record_link_by_attribute_and_index(attribute='Nonexistant', attribute_value='attribute')
        self.assertEqual(context.exception.args[0], "No components with Nonexistant 'attribute' found on page")

    def test_click_record_link_out_of_bounds_index(self) -> None:
        report_body = read_mock_file("nested_dynamic_link_response.json")
        self.custom_locust.set_response(path=self.report_link_uri, status_code=200, body=report_body)
        sail_form = self.task_set.appian.visitor.visit_report(self.report_name, exact_match=False)

        with self.assertRaisesRegex(Exception, "Index: '100' out of range"):
            sail_form.click_record_link_by_attribute_and_index(index=100)

    def test_click_record_link_zero_index(self) -> None:
        report_body = read_mock_file("nested_dynamic_link_response.json")
        self.custom_locust.set_response(path=self.report_link_uri, status_code=200, body=report_body)
        sail_form = self.task_set.appian.visitor.visit_report(self.report_name, exact_match=False)

        with self.assertRaisesRegex(Exception, "Invalid index: '0'. Please enter a positive number. Indexing is 1-based to match SAIL indexing convention"):
            sail_form.click_record_link_by_index(index=0)

    def test_click_record_link_negative_index(self) -> None:
        report_body = read_mock_file("nested_dynamic_link_response.json")
        self.custom_locust.set_response(path=self.report_link_uri, status_code=200, body=report_body)
        sail_form = self.task_set.appian.visitor.visit_report(self.report_name, exact_match=False)

        with self.assertRaisesRegex(Exception, "Invalid index: '-1'. Please enter a positive number"):
            sail_form.click_record_link_by_index(index=-1)


if __name__ == '__main__':
    unittest.main()

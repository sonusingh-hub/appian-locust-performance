from typing import Any, Dict

from ._interactor import _Interactor
from ._locust_error_handler import raises_locust_error
from ._save_request_builder import save_builder
from .helper import find_component_by_type_and_attribute_and_index_in_dict, find_component_by_type_and_attribute_and_index_in_dict
from .uiform import SailUiForm

DESIGN_URI_PATH: str = "/suite/rest/a/applications/latest/app/design"


class _Design:
    def __init__(self, interactor: _Interactor):
        self.interactor = interactor

    @raises_locust_error
    def fetch_design_json(self) -> Dict[str, Any]:
        """
        Fetches the JSON of /design UI

        Returns: JSON Dictionary

        Example:

            >>> design.fetch_design_json()

        """
        headers = self.interactor.setup_sail_headers()
        headers['X-Client-Mode'] = 'DESIGN'
        label = "Design.ApplicationList"
        response = self.interactor.get_page(DESIGN_URI_PATH, headers=headers, label=label)
        response.raise_for_status()
        return response.json()

    @raises_locust_error
    def fetch_application_json(self, app_id: str) -> Dict[str, Any]:
        """
        Fetches the JSON of the UI for a specific application within the /design environment

        Returns: JSON Dictionary

        Example:

            >>> design.fetch_application_json("AADZeglVgAAgfpsAAJsAAAAAAdA")

        """
        application_uri = f"{DESIGN_URI_PATH}/app/{app_id}"
        headers = self.interactor.setup_sail_headers()
        headers['X-Client-Mode'] = 'DESIGN'
        label = f"Design.SelectedApplication.{app_id}"
        response = self.interactor.get_page(application_uri, headers=headers, label=label)
        response.raise_for_status()
        return response.json()

    @raises_locust_error
    def fetch_design_object_json(self, opaque_id: str) -> Dict[str, Any]:
        """
        Fetches the JSON of the UI for a specific object within the /design environment

        Returns: JSON Dictionary

        Example:

             >>> design.fetch_design_object_json("lABD1iTIu_lxy_3T_90Is2fs63uh52xESYi6-fun7FBWshlrBQ0EptlFUdGyIRzSSluPyVdvOhvGgL6aBlnjlkWfQlALYR2aRZ_AIliJ4lc3g")

        """
        headers = self.interactor.setup_sail_headers()
        headers['X-Client-Mode'] = 'DESIGN'
        uri = DESIGN_URI_PATH + '/' + opaque_id
        label = "Design.SelectedObject." + opaque_id[0:10]
        response = self.interactor.get_page(uri, headers=headers, label=label)
        response.raise_for_status()
        return response.json()

    @raises_locust_error
    def find_design_grid(self, state: Dict[str, Any]) -> Dict[str, Any]:
        return find_component_by_type_and_attribute_and_index_in_dict(state, "GridField", "testLabel", "GRID-LABEL")

    def click_expression_editor_toolbar_button(self, button_action: str, post_url: str, state: Dict[str, Any], context: Dict[str, Any], uuid: str,
                                               label: str = None) -> Dict[str, Any]:

        expression_editor_component = find_component_by_type_and_attribute_and_index_in_dict(state, type="ExpressionInfoPanel")["editorWidget"]
        expression = expression_editor_component["value"]

        new_value = {
            "#t": "Dictionary",
            "#v": {
                "actionType": button_action,
                "hasMatchingBracketError": False,
                "launchOrigin": "toolbarButton",
                "queryFnType": "queryRecordType",
                "queryFnStartIndex": 0,
                "queryFnEndIndex": len(expression),
                "value": {
                    "#t": "Text",
                    "#v": expression
                }
            }
        }

        payload = save_builder() \
            .component(expression_editor_component) \
            .context(context) \
            .uuid(uuid) \
            .value(new_value) \
            .build()

        locust_label = label or f'Click \'{button_action}\' Expression Editor Widget Button'

        resp = self.interactor.post_page(
            post_url, payload=payload, label=locust_label
        )
        return resp.json()

    def _create_object(self, ui_form: SailUiForm, link_name: str, object_name: str) -> 'SailUiForm':
        return ui_form.click(link_name)\
            .fill_text_field('Name', object_name)\
            .click('Create')\
            .assert_no_validations_present()\
            .click('Save')

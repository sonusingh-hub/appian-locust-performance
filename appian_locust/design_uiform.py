from typing import Any, Dict

from . import logger
from ._design import _Design
from ._interactor import _Interactor
from ._locust_error_handler import raises_locust_error
from .application_uiform import ApplicationUiForm
from .helper import find_component_by_attribute_in_dict, extract_all_by_label
from .uiform import SailUiForm

log = logger.getLogger(__name__)


class DesignUiForm(SailUiForm):

    def __init__(self, interactor: _Interactor, state: Dict[str, Any], breadcrumb: str = "DesignUi"):
        super().__init__(interactor, state, breadcrumb)
        self.__design = _Design(interactor)

    @raises_locust_error
    def click_application(self, application_name: str) -> 'ApplicationUiForm':
        """
        Click on an application in the /design application grid. Must be on the current page to be clicked.

        Args:
            application_name(str): The name of the application to click on

        Returns (ApplicationUiForm): The latest state of the UiForm, representing the application clicked on
        """
        grid_component = self.__design.find_design_grid(self.state)
        column = find_component_by_attribute_in_dict('label', "Name", grid_component["columns"], throw_attribute_exception=True)
        for index in range(len(column["data"])):
            if column["data"][index] == application_name:
                return ApplicationUiForm(self.interactor, self._dispatch_click(column["links"][index], "DesignGrid"), f"Application.{ application_name }.Ui")
        raise Exception(f"No Application with name { application_name } found in /design grid")

    @raises_locust_error
    def create_application(self, application_name: str) -> 'ApplicationUiForm':
        """
        Creates an application and returns a form within representing the app contents

        Returns: The SAIL UI Form

        """
        app_form = self.__design._create_object(self, link_name='New Application', object_name=application_name)
        app_form.breadcrumb = f"Design.SelectedApplicationByName.{application_name}"
        return ApplicationUiForm(self.interactor, self.state, self.breadcrumb)

    def import_application(self, app_file_path: str, customization_file_path: str = None, inspect_and_import: bool = False) -> None:
        # Open the import modal
        self.click_button("Import")

        # Upload Package
        self.upload_document_to_upload_field("Package (ZIP)", app_file_path)

        # Optionally upload import cust file
        if customization_file_path:
            log.info("Adding customization file")
            self.check_checkbox_by_test_label("propertiesCheckboxField", [1])
            self.upload_document_to_upload_field("Import Customization File (PROPERTIES)", customization_file_path)

        if inspect_and_import:
            log.info("First inspecting and then importing the package")
            self.click_button("Inspect").click_button("Import Package")
        else:
            log.info("Simply importing the package")
            self.click_button("Import")

        self.assert_no_validations_present()

        self.click_button("Close")

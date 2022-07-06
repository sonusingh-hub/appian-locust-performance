from typing import Any, Dict

from ._design import _Design
from ._interactor import _Interactor
from ._locust_error_handler import raises_locust_error
from .design_object_uiform import DesignObjectUiForm
from .helper import find_component_by_attribute_in_dict
from .uiform import SailUiForm


class ApplicationUiForm(SailUiForm):

    def __init__(self, interactor: _Interactor, state: Dict[str, Any], breadcrumb: str = "ApplicationUi"):
        super().__init__(interactor, state, breadcrumb)
        self.__design = _Design(interactor)

    @raises_locust_error
    def click_design_object(self, design_object_name: str) -> DesignObjectUiForm:
        grid_component = self.__design.find_design_grid(self.state)
        link_component = find_component_by_attribute_in_dict('testLabel', design_object_name, grid_component, throw_attribute_exception=True)
        opaque_id = link_component.get("uri").split('/')[-1]
        breadcrumb = "Design.SelectedObject." + opaque_id[0:10] + ".SailUi"
        return DesignObjectUiForm(self.interactor, self.__design.fetch_design_object_json(opaque_id), breadcrumb)

    @raises_locust_error
    def create_record_type(self, record_type_name: str) -> 'ApplicationUiForm':
        """
        Takes an application form and creates a record type with the given name

        Returns: The SAIL UI Form after the record type is created

        """
        self.__design._create_object(self, link_name='Record Type', object_name=record_type_name)
        return self

    @raises_locust_error
    def create_report(self, report_name: str) -> 'ApplicationUiForm':
        """
        Takes an application form and creates a record type with the given name

        Returns: The SAIL UI Form after the record type is created

        """
        self.__design._create_object(self, link_name='Report', object_name=report_name)
        return self

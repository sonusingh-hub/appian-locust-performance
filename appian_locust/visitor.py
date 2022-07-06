from .application_uiform import ApplicationUiForm
from .design_object_uiform import DesignObjectUiForm
from .design_uiform import DesignUiForm
from .uiform import SailUiForm
from ._design import _Design
from ._interactor import _Interactor
from ._reports import _Reports
from .helper import format_label


class Visitor:
    def __init__(self, interactor: _Interactor):
        self.__interactor = interactor
        self.__reports = _Reports(self.__interactor)
        self.__design = _Design(self.__interactor)

    def visit_report(self, report_name: str, exact_match: bool = True) -> 'SailUiForm':
        """
        Navigate to a report and return a SailUiForm for that report's UI

        Args:
            report_name (str): Name of the report to be called.
            exact_match (bool, optional): Should report name match exactly or to be partial match. Default : True

        Returns (SailUiForm): Response of report's Get UI call in SailUiForm

        """
        breadcrumb = f'Reports.SailUi.{format_label(report_name, "::", 0)}'
        return SailUiForm(self.__interactor, self.__reports.fetch_report_json(report_name, exact_match), breadcrumb=breadcrumb)

    def visit_design(self) -> DesignUiForm:
        return DesignUiForm(self.__interactor, self.__design.fetch_design_json(), breadcrumb="Design.ApplicationList.SailUi")

    def visit_application(self, application_id: str) -> ApplicationUiForm:
        breadcrumb = f"Design.SelectedApplication.{application_id}.SailUi"
        return ApplicationUiForm(self.__interactor, self.__design.fetch_application_json(application_id), breadcrumb)

    def visit_design_object(self, opaque_id: str) -> DesignObjectUiForm:
        breadcrumb = "Design.SelectedObject." + opaque_id[0:10] + ".SailUi"
        return DesignObjectUiForm(self.__interactor, self.__design.fetch_design_object_json(opaque_id), breadcrumb)

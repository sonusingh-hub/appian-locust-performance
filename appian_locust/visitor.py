from appian_locust.record_uiform import RecordInstanceUiForm
from .application_uiform import ApplicationUiForm
from .design_object_uiform import DesignObjectUiForm
from .design_uiform import DesignUiForm
from .uiform import SailUiForm
from ._design import _Design
from ._interactor import _Interactor
from ._records import _Records
from ._reports import _Reports
from .helper import format_label


class Visitor:
    def __init__(self, interactor: _Interactor):
        self.__interactor = interactor
        self.__reports = _Reports(self.__interactor)
        self.__design = _Design(self.__interactor)
        self.__records = _Records(self.__interactor)

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

    def visit_record_instance(self, record_type: str = "", record_name: str = "", view_url_stub: str = "", exact_match: bool = False, summary_view: bool = True) -> RecordInstanceUiForm:
        """
        Navigate to a specific record and return a RecordUiForm

        Args:
            record_type (str): Record Type Name. If not specified, a random record type will be selected.
            record_name (str): Name of the record to be called. If not specified, a random record will be selected.
            view_url_stub (str, optional): page/tab to be visited in the record. If not specified, "summary" dashboard will be selected.
            exact_match (bool, optional): Should record type and record name matched exactly as it is or partial match.
            summary_view (bool, optional): Should the Record UI be returned in Summary View, if false will return Header View

        Returns (RecordUiForm): The UI for the record instance

        """
        form_json = self.__records.visit_record_instance(record_type, record_name, view_url_stub=view_url_stub, exact_match=exact_match)
        breadcrumb = f'Records.{record_type}.{format_label(record_name, "::", 0)}.SailUi'
        return RecordInstanceUiForm(self.__interactor, form_json, summary_view=summary_view, breadcrumb=breadcrumb)

    def visit_record_type(self, record_type: str = "", exact_match: bool = False, is_mobile: bool = False) -> SailUiForm:
        """
        This function calls the API for the specific record type and returns a SAIL form representing the list of records for that record type.

        Args:
            record_type (str): Record Type Name. If not specified, a random record type will be selected.
            exact_match (bool, optional): Should record type and record name matched exactly as it is or partial match.

        Returns (SailUiForm): UI representing list of records for that record type
        """
        form_json = self.__records.visit_record_type(record_type, exact_match=exact_match, is_mobile=is_mobile)
        breadcrumb = f'Records.{record_type}.SailUi'
        return SailUiForm(self.__interactor, form_json, breadcrumb=breadcrumb)

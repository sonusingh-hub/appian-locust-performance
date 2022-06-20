from ._interactor import _Interactor
from ._reports import _Reports
from .helper import format_label
from .uiform import SailUiForm


class Visitor:
    def __init__(self, interactor: _Interactor):
        self.__interactor = interactor
        self.__reports = _Reports(self.__interactor)

    def visit_report(self, report_name: str, exact_match: bool = True) -> 'SailUiForm':
        """
        Navigate to a report and return a SailUiForm for that report's UI
        Args:
            report_name (str): Name of the report to be called.
            exact_match (bool, optional): Should report name match exactly or to be partial match. Default : True

        Returns (SailUiForm): Response of report's Get UI call in SailUiForm

        """
        report_form_uri = self.__reports.get_report_form_uri(report_name, exact_match)
        report_json = self.__reports.fetch_report_json(report_name, report_form_uri)

        breadcrumb = f'Reports.SailUi.{format_label(report_name, "::", 0)}'
        return SailUiForm(self.__interactor, report_json, report_form_uri, breadcrumb=breadcrumb)

from appian_locust.record_uiform import RecordInstanceUiForm
from .application_uiform import ApplicationUiForm
from .design_object_uiform import DesignObjectUiForm
from .design_uiform import DesignUiForm
from .record_list_uiform import RecordListUiForm
from .uiform import SailUiForm
from ._design import _Design
from ._interactor import _Interactor
from ._records import _Records
from ._reports import _Reports
from ._sites import _Sites, PageType
from ._tasks import _Tasks
from .helper import format_label


class Visitor:
    def __init__(self, interactor: _Interactor):
        self.__interactor = interactor
        self._tasks = _Tasks(self.__interactor)
        self.__reports = _Reports(self.__interactor)
        self.__design = _Design(self.__interactor)
        self.__records = _Records(self.__interactor)
        self.__sites = _Sites(self.__interactor)

    def visit_task(self, task_name: str, exact_match: bool = True, locust_request_label: str = "") -> SailUiForm:
        """
        Gets the SailUiForm given a task name

        Args:
            task_name (str): Name of the task to search for
            exact_match (bool, optional): Whether or not a full match is returned. Defaults to True.
            locust_request_label (str, optional): label to be used within locust

        Returns:
            SailUiForm: SAIL form for the task
        """
        initial_task_resp: dict = self._tasks.get_task(task_name, exact_match)
        children = initial_task_resp.get("content", {}).get("children", [])
        task_title = children[0]

        if not locust_request_label:
            breadcrumb = f"Tasks.{task_title}"
        else:
            breadcrumb = locust_request_label
        return SailUiForm(self.__interactor, self._tasks.get_task_form_json(task_name=task_title, locust_request_label=breadcrumb, exact_match=False), breadcrumb=breadcrumb)

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

    def visit_record_type(self, record_type: str = "", exact_match: bool = False, is_mobile: bool = False) -> RecordListUiForm:
        """
        This function calls the API for the specific record type and returns a SAIL form representing the list of records for that record type.

        Args:
            record_type (str): Record Type Name. If not specified, a random record type will be selected.
            exact_match (bool, optional): Should record type and record name matched exactly as it is or partial match.

        Returns (SailUiForm): UI representing list of records for that record type
        """
        form_json = self.__records.visit_record_type(record_type, exact_match=exact_match, is_mobile=is_mobile)
        breadcrumb = f'Records.{record_type}.RecordListUi'
        return RecordListUiForm(self.__interactor, form_json, breadcrumb=breadcrumb)

    def visit_site(self, site_name: str, page_name: str) -> 'SailUiForm':
        """
        Get a SailUiForm for a Task, Report or Action

        Args:
            site_name(str): Site where the page exists
            page_name(str): Page to navigate to

        Returns: SailUiForm

        Example:
            >>> self.appian.visitor.visit_site("site_name","page_name")

        """
        form_json = self.__sites.fetch_site_tab_json(site_name, page_name)

        breadcrumb = f"Sites.{site_name}.{page_name}.SailUi"
        return SailUiForm(self.__interactor, form_json, breadcrumb=breadcrumb)

    def visit_site_recordlist(self, site_name: str, page_name: str) -> 'RecordListUiForm':
        """
        Get a RecordListUiForm for a record list page on a site

        Args:
            site_name(str): Site where the page exists
            page_name(str): Page to navigate to

        Returns: SailUiForm

        Example:
            >>> self.appian.visitor.visit_site_recordlist("site_name","page_name")

        """
        page_type = self.__sites.get_site_page_type(site_name, page_name)
        if page_type != PageType.RECORD:
            raise Exception(f"Page {page_name} on site {site_name} is not of type record")
        form_json = self.__sites.fetch_site_tab_json(site_name, page_name)

        breadcrumb = f"Sites.{site_name}.{page_name}.SailUi"
        return RecordListUiForm(self.__interactor, form_json, breadcrumb=breadcrumb)

    def visit_site_recordlist_and_get_random_record_form(self, site_name: str, page_name: str) -> RecordInstanceUiForm:
        """
        Navigates to a site page that is a recordlist then clicks on a random record instance on the first page

        Args:
            site_name: Site Url stub
            page_name: Page Url stub

        Returns: RecordInstanceUiForm
        """

        site_page_json_response = self.__sites.fetch_site_tab_record_json(site_name, page_name)
        summary_view = site_page_json_response.get("feed") is not None
        breadcrumb = f"Sites.{site_name}.{page_name}.SailUi"
        return RecordInstanceUiForm(self.__interactor, site_page_json_response, summary_view=summary_view, breadcrumb=breadcrumb)

from .news_info import NewsInfo
from .actions_info import ActionsInfo
from .records_info import RecordsInfo
from .reports_info import ReportsInfo
from .sites_info import SitesInfo
from .tasks_info import TasksInfo
from ._actions import _Actions
from ._interactor import _Interactor
from ._news import _News
from ._records import _Records
from ._reports import _Reports
from ._sites import _Sites
from ._tasks import _Tasks


class TempoNavigator:
    """
    Used for navigating the primary tabs on tempo to provide metadata on the content available for interaction.
    """

    def __init__(self, interactor: _Interactor, tasks: _Tasks, reports: _Reports, actions: _Actions, records: _Records,
                 sites: _Sites):
        self.__interactor = interactor
        self.__tasks = tasks
        self.__reports = reports
        self.__records = records
        self.__sites = sites
        self.__actions = actions
        self.__news = _News(interactor)

    def navigate_to_news_and_get_info(self) -> NewsInfo:
        """
        Navigate to the News tab in Tempo and gather information about available news entries
        """
        return NewsInfo(self.__news)

    def navigate_to_records_and_get_info(self) -> RecordsInfo:
        """
        Navigate to the records tab in Tempo and gather information about available record types
        """
        return RecordsInfo(records=self.__records)

    def navigate_to_actions_and_get_info(self) -> ActionsInfo:
        """
        Navigate to the actions tab in Tempo and gather information about available actions
        """
        return ActionsInfo(self.__actions)

    def navigate_to_tasks_and_get_info(self) -> TasksInfo:
        """
        Navigate to the tasks tab in Tempo and gather information about available tasks
        """
        return TasksInfo(self.__tasks)

    def navigate_to_reports_and_get_info(self) -> ReportsInfo:
        """
        Navigate to the reports tab in Tempo and gather information about available reports
        """
        return ReportsInfo(self.__reports)

    def get_sites_info(self) -> SitesInfo:
        """
        Get Site metadata object
        """
        return SitesInfo(self.__sites)

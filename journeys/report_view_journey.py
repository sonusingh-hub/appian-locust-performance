from locust import task

from journeys.base_journey import BaseJourney
from utils.waits import think_time
from data.data_engine import DataEngine
from pages.home_page import HomePage
from pages.reports_page import ReportsPage


class ReportViewJourney(BaseJourney):

    @task
    def view_report_flow(self):
        home = HomePage(self)
        reports = ReportsPage(self)

        uiform = home.open()
        if not uiform:
            return

        think_time()

        uiform = home.select_country(
            uiform,
            DataEngine.country()
        )

        think_time()

        uiform = reports.open_fleet_schedule()
        if not uiform:
            return

        think_time()

        uiform = reports.select_month(
            uiform,
            DataEngine.month()
        )

        think_time()

        home.open()
        think_time()
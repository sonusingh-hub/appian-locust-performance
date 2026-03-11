from locust import task
from appian_locust import AppianTaskSet

from utils.waits import think_time
from data.data_engine import DataEngine
from pages.home_page import HomePage
from pages.alerts_page import AlertsPage
from pages.reports_page import ReportsPage


class AnalystJourney(AppianTaskSet):

    def on_start(self):
        super().on_start()

        if not hasattr(self, "user_context"):
            self.user_context = {}

    @task
    def analyst_flow(self):

        # HOME
        home = HomePage(self)
        uiform = home.open()

        if not uiform:
            return

        think_time()

        home.select_country(
            uiform,
            DataEngine.country()
        )

        think_time()

        # ALERTS
        alerts = AlertsPage(self)
        uiform = alerts.open()

        if not uiform:
            return

        think_time()

        alerts.search_record(
            uiform,
            DataEngine.company()
        )

        think_time()

        alerts.filter_country(
            uiform,
            DataEngine.country()
        )

        think_time()

        alerts.export_report(uiform)

        think_time()

        # REPORTS
        reports = ReportsPage(self)
        uiform = reports.open_fleet_schedule()

        if not uiform:
            return

        think_time()

        reports.select_month(
            uiform,
            DataEngine.month()
        )

        think_time()

        # BACK TO HOME
        home.open()

        think_time()
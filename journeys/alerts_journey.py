from locust import task

from journeys.base_journey import BaseJourney
from utils.waits import think_time
from data.data_engine import DataEngine
from pages.alerts_page import AlertsPage


class AlertsJourney(BaseJourney):

    @task
    def alerts_flow(self):
        alerts = AlertsPage(self)

        uiform = alerts.open()
        if not uiform:
            return

        think_time()

        uiform = alerts.search_record(
            uiform,
            DataEngine.company()
        )

        think_time()

        uiform = alerts.click_search_box(uiform)

        think_time()

        uiform = alerts.refresh_grid(uiform)

        think_time()

        uiform = alerts.clear_filters(uiform)

        think_time()
from locust import task
import random

from journeys.base_journey import BaseJourney
from utils.waits import think_time, small_wait, reading_pause
from data.data_engine import DataEngine
from pages.vehicle_search_page import VehicleSearchPage


class VehicleSearchJourney(BaseJourney):
    journey_name = "vehicle_search"

    def _open_random_reports_page(self, page, uiform):
        navigation_actions = [
            page.open_alerts,
            page.open_fleet_schedule,
            page.open_vehicle_on_order,
            page.open_imminent_expiry,
            page.open_sustainability,
            page.open_vehicle_utilisation,
            page.open_service_overdue,
        ]

        open_action = random.choice(navigation_actions)
        return open_action(uiform)

    @task
    def vehicle_search_flow(self):
        page = VehicleSearchPage(self)

        uiform = page.open()
        if not uiform:
            return

        think_time()
        small_wait()

        uiform = self._open_random_reports_page(page, uiform)
        if not uiform:
            return

        # 8% chance the user browses the report page and navigates away
        # without continuing to the vehicle search — normal user behaviour.
        if self._should_abandon(0.08):
            return

        reading_pause(rows=20)

        uiform = page.open_vehicle_search(uiform)
        if not uiform:
            return

        think_time()

        uiform = page.select_country(uiform, "Australia")
        if not uiform:
            return

        think_time()

        reg_vals = self._get_page_filter_values(
            "vehicle_search_reg",
            lambda: {"registration": DataEngine.registration()},
        )
        uiform = page.fill_registration(uiform, reg_vals["registration"])

        think_time()

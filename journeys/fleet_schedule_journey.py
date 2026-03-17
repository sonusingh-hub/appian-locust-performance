from locust import task
import random

from journeys.base_journey import BaseJourney
from utils.waits import think_time, small_wait
from data.data_engine import DataEngine
from pages.fleet_schedule_page import FleetSchedulePage


class FleetScheduleJourney(BaseJourney):
    journey_name = "fleet-schedule"

    def _multi_select_count(self, max_count=4):
        return random.randint(1, max_count)

    def _open_fleet_schedule(self):
        page = FleetSchedulePage(self)

        uiform = page.open()
        if not uiform:
            return page, None

        think_time()
        small_wait()
        return page, uiform

    def _return_to_fleet_schedule(self, page):
        """Return to Fleet Schedule using deterministic navigation.

        Back click from card detail pages is intermittently returning 500 in
        this environment, so we re-open the page to keep task execution stable.
        """
        uiform = page.open()
        if not uiform:
            return None

        think_time()
        small_wait()
        return uiform

    def _apply_fleet_schedule_filters(self, page, uiform):
        # Reuse shared global filters state so behaviour matches all report pages.
        if not self.filter_state.is_applied:
            uiform = page.apply_global_filters(
                uiform,
                self.filter_state,
                countries=DataEngine.home_country_list(),
                client_groups=DataEngine.home_client_groups(),
                client_names=DataEngine.home_client_names(),
                bill_to_values=DataEngine.home_bill_to(),
            )
            if not uiform:
                return None

            think_time()

        uiform = page.select_month(uiform, DataEngine.month())
        if not uiform:
            return None

        think_time()

        uiform = page.select_product(
            uiform,
            DataEngine.fleet_schedule_products(count=self._multi_select_count(4)),
        )
        if not uiform:
            return None

        think_time()

        uiform = page.select_vehicle_type(
            uiform,
            DataEngine.vehicle_type_list(count=self._multi_select_count(4)),
        )
        if not uiform:
            return None

        think_time()

        uiform = page.select_imminent_expiry(uiform, DataEngine.imminent_expiry())
        if not uiform:
            return None

        think_time()

        uiform = page.select_power_train(
            uiform,
            DataEngine.power_train_list(count=self._multi_select_count(4)),
        )
        if not uiform:
            return None

        think_time()
        return uiform

    def _open_card_flow(self, open_card_action, search_value=None, export=False):
        page, uiform = self._open_fleet_schedule()
        if not uiform:
            return

        uiform = self._apply_fleet_schedule_filters(page, uiform)
        if not uiform:
            return

        uiform = open_card_action(page, uiform)
        if not uiform:
            return

        think_time()

        if search_value is not None:
            uiform = page.search_record(uiform, search_value)
            if not uiform:
                return

            think_time()

            uiform = page.click_search_box(uiform)
            if not uiform:
                return

            think_time()

        if export:
            uiform = page.export_report(uiform)
            if not uiform:
                return

            think_time()

        uiform = self._return_to_fleet_schedule(page)
        if not uiform:
            return

        think_time()

    @task(4)
    def fleet_schedule_filter_flow(self):
        page, uiform = self._open_fleet_schedule()
        if not uiform:
            return

        uiform = self._apply_fleet_schedule_filters(page, uiform)
        if not uiform:
            return

    @task(2)
    def fleet_schedule_active_vehicles_flow(self):
        self._open_card_flow(
            lambda page, ui: page.open_active_vehicles(ui),
            search_value="AstraZeneca",
            export=True,
        )

    @task(2)
    def fleet_schedule_vehicle_utilisation_card_flow(self):
        self._open_card_flow(
            lambda page, ui: page.open_vehicle_utilisation(ui),
            search_value="",
            export=True,
        )

    @task(1)
    def fleet_schedule_imminent_expiry_card_flow(self):
        self._open_card_flow(
            lambda page, ui: page.open_imminent_expiry_card(ui),
            search_value="Colgate",
            export=False,
        )

    @task(1)
    def fleet_schedule_registration_overdue_card_flow(self):
        page, uiform = self._open_fleet_schedule()
        if not uiform:
            return

        uiform = self._apply_fleet_schedule_filters(page, uiform)
        if not uiform:
            return

        uiform = page.open_registration_overdue(uiform)
        if not uiform:
            return

        think_time()

        # Keep sequence close to the recorder actions.
        uiform = page.search_record(uiform, "")
        if not uiform:
            return

        uiform = page.search_record(uiform, "Hills")
        if not uiform:
            return

        think_time()

        uiform = page.click_search_box(uiform)
        if not uiform:
            return

        think_time()

        uiform = page.search_record(uiform, "")
        if not uiform:
            return

        think_time()

        uiform = self._return_to_fleet_schedule(page)
        if not uiform:
            return

        think_time()

    @task(1)
    def fleet_schedule_reset_global_filters_flow(self):
        page, uiform = self._open_fleet_schedule()
        if not uiform:
            return

        uiform = page.reset_global_filters(uiform, self.filter_state)
        if not uiform:
            return

        think_time()

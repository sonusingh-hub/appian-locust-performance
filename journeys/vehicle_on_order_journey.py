from locust import task
import random

from journeys.base_journey import BaseJourney
from utils.waits import think_time, small_wait
from data.data_engine import DataEngine
from pages.vehicle_on_order_page import VehicleOnOrderPage


class VehicleOnOrderJourney(BaseJourney):
    journey_name = "vehicles-on-order"

    def _multi_select_count(self, max_count=4):
        return random.randint(1, max_count)

    def _open_vehicle_on_order(self):
        page = VehicleOnOrderPage(self)

        uiform = page.open()
        if not uiform:
            return page, None

        think_time()
        small_wait()
        return page, uiform

    def _return_to_vehicle_on_order(self, page):
        """Return to Vehicles On Order with deterministic navigation.

        Back click from card detail pages can intermittently
        return 500, so we re-open the page for stable task execution.
        """
        uiform = page.open()
        if not uiform:
            return None

        think_time()
        small_wait()
        return uiform

    def _apply_vehicle_on_order_filters(self, page, uiform):
        """Apply global filters then page-specific filters in cascade order."""
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

        filter_values = self._get_page_filter_values(
            "vehicle_on_order",
            lambda: {
                "product": DataEngine.vehicle_on_order_products(count=self._multi_select_count(4)),
                "vehicle_type": DataEngine.vehicle_on_order_vehicle_types(count=self._multi_select_count(4)),
                "power_train": DataEngine.power_train_list(count=self._multi_select_count(4)),
                "expected_delivery": DataEngine.expected_delivery(),
            },
        )

        uiform = page.select_product(
            uiform,
            filter_values["product"],
        )
        if not uiform:
            return None

        think_time()

        uiform = page.select_vehicle_type(
            uiform,
            filter_values["vehicle_type"],
        )
        if not uiform:
            return None

        think_time()

        uiform = page.select_power_train(
            uiform,
            filter_values["power_train"],
        )
        if not uiform:
            return None

        think_time()

        uiform = page.select_expected_delivery(uiform, filter_values["expected_delivery"])
        if not uiform:
            return None

        think_time()
        return uiform

    def _open_card_flow(self, open_card_action, search_value=None, export=False):
        page, uiform = self._open_vehicle_on_order()
        if not uiform:
            return

        uiform = self._apply_vehicle_on_order_filters(page, uiform)
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

    @task(4)
    def vehicle_on_order_filter_flow(self):
        page, uiform = self._open_vehicle_on_order()
        if not uiform:
            return

        uiform = self._apply_vehicle_on_order_filters(page, uiform)
        if not uiform:
            return

    @task(2)
    def vehicle_on_order_vehicles_on_order_card_flow(self):
        self._open_card_flow(
            lambda page, ui: page.open_vehicles_on_order(ui),
            search_value="Nestle",
            export=True,
        )

    @task(2)
    def vehicle_on_order_funded_vehicles_card_flow(self):
        self._open_card_flow(
            lambda page, ui: page.open_funded_vehicles_on_order(ui),
            search_value="",
            export=False,
        )

    @task(1)
    def vehicle_on_order_delivery_overdue_card_flow(self):
        self._open_card_flow(
            lambda page, ui: page.open_delivery_overdue(ui),
        )

    @task(1)
    def vehicle_on_order_reset_global_filters_flow(self):
        page, uiform = self._open_vehicle_on_order()
        if not uiform:
            return

        uiform = page.reset_global_filters(uiform, self.filter_state)
        if not uiform:
            return

        self._clear_page_filter_values("vehicle_on_order")
        think_time()

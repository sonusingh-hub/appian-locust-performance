from locust import task
import random

from journeys.base_journey import BaseJourney
from utils.waits import think_time, small_wait
from data.data_engine import DataEngine
from pages.sustainability_page import SustainabilityPage


class SustainabilityJourney(BaseJourney):
    journey_name = "sustainability"

    def _multi_select_count(self, max_count=4):
        return random.randint(1, max_count)

    def _open_sustainability(self):
        page = SustainabilityPage(self)

        uiform = page.open()
        if not uiform:
            return page, None

        think_time()
        small_wait()
        return page, uiform

    def _apply_sustainability_filters(self, page, uiform):
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
            "sustainability",
            lambda: {
                "product": DataEngine.sustainability_products(count=self._multi_select_count(4)),
                "vehicle_type": DataEngine.vehicle_type_list(count=self._multi_select_count(4)),
                "power_train": DataEngine.power_train_list(count=self._multi_select_count(4)),
                "start_date": DataEngine.sustainability_start_date(),
                "end_date": DataEngine.sustainability_end_date(),
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

        start_date = filter_values["start_date"]
        uiform = page.set_start_date(
            uiform,
            start_date["year"],
            start_date["month"],
            start_date["day"],
        )
        if not uiform:
            return None

        think_time()

        end_date = filter_values["end_date"]
        uiform = page.set_end_date(
            uiform,
            end_date["year"],
            end_date["month"],
            end_date["day"],
        )
        if not uiform:
            return None

        think_time()
        return uiform

    @task(4)
    def sustainability_filter_flow(self):
        page, uiform = self._open_sustainability()
        if not uiform:
            return

        uiform = self._apply_sustainability_filters(page, uiform)
        if not uiform:
            return

    @task(1)
    def sustainability_reset_global_filters_flow(self):
        page, uiform = self._open_sustainability()
        if not uiform:
            return

        uiform = page.reset_global_filters(uiform, self.filter_state)
        if not uiform:
            return

        self._clear_page_filter_values("sustainability")
        think_time()

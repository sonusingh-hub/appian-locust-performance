from locust import task
import random

from journeys.base_journey import BaseJourney
from utils.waits import think_time, small_wait
from data.data_engine import DataEngine
from pages.service_overdue_page import ServiceOverduePage


class ServiceOverdueJourney(BaseJourney):
    journey_name = "service-overdue"

    def _multi_select_count(self, max_count=4):
        return random.randint(1, max_count)

    def _open_service_overdue(self):
        page = ServiceOverduePage(self)

        uiform = page.open()
        if not uiform:
            return page, None

        think_time()
        small_wait()
        return page, uiform

    def _return_to_service_overdue(self, page):
        """Return with deterministic navigation.

        Back click from card detail pages can intermittently return 500,
        so we re-open the page for stable task execution.
        """
        uiform = page.open()
        if not uiform:
            return None

        think_time()
        small_wait()
        return uiform

    def _apply_service_overdue_filters(self, page, uiform):
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
            "service_overdue",
            lambda: {
                "month": DataEngine.service_overdue_month(),
                "product": DataEngine.service_overdue_products(count=self._multi_select_count(4)),
                "overdue_by": DataEngine.overdue_by(),
                "vehicle_type": DataEngine.vehicle_type_list(count=self._multi_select_count(4)),
                "power_train": DataEngine.power_train_list(count=self._multi_select_count(4)),
                "maintenance_included": DataEngine.maintenance_included(),
            },
        )

        uiform = page.select_month(uiform, filter_values["month"])
        if not uiform:
            return None

        think_time()

        uiform = page.select_product(
            uiform,
            filter_values["product"],
        )
        if not uiform:
            return None

        think_time()

        uiform = page.select_overdue_by(uiform, filter_values["overdue_by"])
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

        uiform = page.select_maintenance_included(uiform, filter_values["maintenance_included"])
        if not uiform:
            return None

        think_time()
        return uiform

    def _open_card_flow(self, open_card_action, search_value=None, clear_search=False, export=False):
        page, uiform = self._open_service_overdue()
        if not uiform:
            return

        uiform = self._apply_service_overdue_filters(page, uiform)
        if not uiform:
            return

        uiform = open_card_action(page, uiform)
        if not uiform:
            return

        think_time()

        if export:
            uiform = page.export_report(uiform)
            if not uiform:
                return

            think_time()

        if search_value is not None:
            uiform = page.search_detail_record(uiform, search_value)
            if not uiform:
                return

            think_time()

            uiform = page.click_detail_search_box(uiform)
            if not uiform:
                return

            think_time()

        if clear_search:
            uiform = page.search_detail_record(uiform, "")
            if not uiform:
                return

            think_time()

    @task(4)
    def service_overdue_filter_flow(self):
        page, uiform = self._open_service_overdue()
        if not uiform:
            return

        uiform = self._apply_service_overdue_filters(page, uiform)
        if not uiform:
            return

    @task(2)
    def service_overdue_total_overdue_now_card_flow(self):
        self._open_card_flow(
            lambda page, ui: page.open_total_overdue_now(ui),
            search_value="Colgate",
            clear_search=True,
            export=True,
        )

    @task(2)
    def service_overdue_maximum_days_overdue_card_flow(self):
        self._open_card_flow(
            lambda page, ui: page.open_maximum_days_overdue(ui),
        )

    @task(1)
    def service_overdue_maximum_kms_overdue_card_flow(self):
        self._open_card_flow(
            lambda page, ui: page.open_maximum_kms_overdue(ui),
        )

    @task(1)
    def service_overdue_reset_global_filters_flow(self):
        page, uiform = self._open_service_overdue()
        if not uiform:
            return

        uiform = page.reset_global_filters(uiform, self.filter_state)
        if not uiform:
            return

        self._clear_page_filter_values("service_overdue")
        think_time()
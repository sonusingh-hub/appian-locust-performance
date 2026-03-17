from locust import task
import random

from journeys.base_journey import BaseJourney
from utils.waits import think_time, small_wait
from data.data_engine import DataEngine

from pages.alerts_page import AlertsPage
from pages.fleet_schedule_page import FleetSchedulePage
from pages.vehicle_on_order_page import VehicleOnOrderPage
from pages.imminent_expiry_page import ImminentExpiryPage
from pages.sustainability_page import SustainabilityPage
from pages.vehicle_utilisation_page import VehicleUtilisationPage
from pages.service_overdue_page import ServiceOverduePage


class FilterJourney(BaseJourney):
    journey_name = "filter"

    def _multi_select_count(self, max_count=4):
        return random.randint(1, max_count)

    # ---------- Page Open Helpers ----------

    def _open_alerts(self):
        page = AlertsPage(self)
        uiform = page.open()
        if not uiform:
            return page, None

        think_time()
        small_wait()
        return page, uiform

    def _open_fleet_schedule(self):
        page = FleetSchedulePage(self)
        uiform = page.open()
        if not uiform:
            return page, None

        think_time()
        small_wait()
        return page, uiform

    def _open_vehicle_on_order(self):
        page = VehicleOnOrderPage(self)
        uiform = page.open()
        if not uiform:
            return page, None

        think_time()
        small_wait()
        return page, uiform

    def _open_imminent_expiry(self):
        page = ImminentExpiryPage(self)
        uiform = page.open()
        if not uiform:
            return page, None

        think_time()
        small_wait()
        return page, uiform

    def _open_sustainability(self):
        page = SustainabilityPage(self)
        uiform = page.open()
        if not uiform:
            return page, None

        think_time()
        small_wait()
        return page, uiform

    def _open_vehicle_utilisation(self):
        page = VehicleUtilisationPage(self)
        uiform = page.open()
        if not uiform:
            return page, None

        think_time()
        small_wait()
        return page, uiform

    def _open_service_overdue(self):
        page = ServiceOverduePage(self)
        uiform = page.open()
        if not uiform:
            return page, None

        think_time()
        small_wait()
        return page, uiform

    def _apply_global_filters_if_needed(self, page, uiform):
        if not uiform:
            return None

        if self.filter_state.is_applied:
            return uiform

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
        return uiform

    # ---------- Filter Flows ----------

    @task(2)
    def alerts_filter_flow(self):
        page, uiform = self._open_alerts()
        if not uiform:
            return

        uiform = self._apply_global_filters_if_needed(page, uiform)
        if not uiform:
            return

        uiform = page.search_record(uiform, DataEngine.company())
        if not uiform:
            return

        think_time()

        uiform = page.click_search_box(uiform)
        if not uiform:
            return

        think_time()

        uiform = page.filter_country(uiform, DataEngine.country())
        if not uiform:
            return

        think_time()

    @task(5)
    def fleet_schedule_filter_flow(self):
        page, uiform = self._open_fleet_schedule()
        if not uiform:
            return

        uiform = self._apply_global_filters_if_needed(page, uiform)
        if not uiform:
            return

        uiform = page.open_fleet_schedule_card(uiform, "Active Vehicles")
        if not uiform:
            return

        think_time()

        uiform = page.select_month(uiform, DataEngine.month())
        if not uiform:
            return

        think_time()

        uiform = page.select_product(
            uiform,
            DataEngine.fleet_schedule_products(count=self._multi_select_count(4)),
        )
        if not uiform:
            return

        think_time()

        uiform = page.select_vehicle_type(
            uiform,
            DataEngine.vehicle_type_list(count=self._multi_select_count(4)),
        )
        if not uiform:
            return

        think_time()

        uiform = page.select_imminent_expiry(uiform, DataEngine.imminent_expiry())
        if not uiform:
            return

        think_time()

        uiform = page.select_power_train(
            uiform,
            DataEngine.power_train_list(count=self._multi_select_count(4)),
        )
        if not uiform:
            return

        think_time()

    @task(5)
    def vehicle_on_order_filter_flow(self):
        page, uiform = self._open_vehicle_on_order()
        if not uiform:
            return

        uiform = self._apply_global_filters_if_needed(page, uiform)
        if not uiform:
            return

        uiform = page.open_vehicles_on_order(uiform)
        if not uiform:
            return

        think_time()

        uiform = page.select_product(
            uiform,
            DataEngine.vehicle_on_order_products(count=self._multi_select_count(4)),
        )
        if not uiform:
            return

        think_time()

        uiform = page.select_vehicle_type(
            uiform,
            DataEngine.vehicle_on_order_vehicle_types(count=self._multi_select_count(4)),
        )
        if not uiform:
            return

        think_time()

        uiform = page.select_power_train(
            uiform,
            DataEngine.power_train_list(count=self._multi_select_count(4)),
        )
        if not uiform:
            return

        think_time()

        uiform = page.select_expected_delivery(uiform, DataEngine.expected_delivery())
        if not uiform:
            return

        think_time()

    @task(5)
    def vehicle_utilisation_filter_flow(self):
        page, uiform = self._open_vehicle_utilisation()
        if not uiform:
            return

        uiform = self._apply_global_filters_if_needed(page, uiform)
        if not uiform:
            return

        uiform = page.open_vehicle_utilisation(uiform)
        if not uiform:
            return

        think_time()

        uiform = page.select_month(uiform, DataEngine.vehicle_utilisation_month())
        if not uiform:
            return

        think_time()

        uiform = page.select_product(
            uiform,
            DataEngine.vehicle_utilisation_products(count=self._multi_select_count(4)),
        )
        if not uiform:
            return

        think_time()

        uiform = page.select_vehicle_type(
            uiform,
            DataEngine.vehicle_type_list(count=self._multi_select_count(4)),
        )
        if not uiform:
            return

        think_time()

        uiform = page.select_imminent_expiry(uiform, DataEngine.imminent_expiry())
        if not uiform:
            return

        think_time()

        uiform = page.select_power_train(
            uiform,
            DataEngine.power_train_list(count=self._multi_select_count(4)),
        )
        if not uiform:
            return

        think_time()

    @task(4)
    def service_overdue_filter_flow(self):
        page, uiform = self._open_service_overdue()
        if not uiform:
            return

        uiform = self._apply_global_filters_if_needed(page, uiform)
        if not uiform:
            return

        uiform = page.open_total_overdue_now(uiform)
        if not uiform:
            return

        think_time()

        uiform = page.select_month(uiform, DataEngine.service_overdue_month())
        if not uiform:
            return

        think_time()

        uiform = page.select_product(
            uiform,
            DataEngine.service_overdue_products(count=self._multi_select_count(4)),
        )
        if not uiform:
            return

        think_time()

        uiform = page.select_overdue_by(uiform, DataEngine.overdue_by())
        if not uiform:
            return

        think_time()

        uiform = page.select_vehicle_type(
            uiform,
            DataEngine.vehicle_type_list(count=self._multi_select_count(4)),
        )
        if not uiform:
            return

        think_time()

        uiform = page.select_power_train(
            uiform,
            DataEngine.power_train_list(count=self._multi_select_count(4)),
        )
        if not uiform:
            return

        think_time()

        uiform = page.select_maintenance_included(uiform, DataEngine.maintenance_included())
        if not uiform:
            return

        think_time()

    @task(4)
    def imminent_expiry_filter_flow(self):
        page, uiform = self._open_imminent_expiry()
        if not uiform:
            return

        uiform = self._apply_global_filters_if_needed(page, uiform)
        if not uiform:
            return

        uiform = page.open_imminent_expiry_card(uiform)
        if not uiform:
            return

        think_time()

        uiform = page.select_month(uiform, DataEngine.imminent_expiry_month())
        if not uiform:
            return

        think_time()

        uiform = page.select_product(
            uiform,
            DataEngine.imminent_expiry_products(count=self._multi_select_count(4)),
        )
        if not uiform:
            return

        think_time()

        uiform = page.select_vehicle_type(
            uiform,
            DataEngine.vehicle_type_list(count=self._multi_select_count(4)),
        )
        if not uiform:
            return

        think_time()

        uiform = page.select_imminent_expiry(uiform, DataEngine.imminent_expiry())
        if not uiform:
            return

        think_time()

        uiform = page.select_power_train(
            uiform,
            DataEngine.power_train_list(count=self._multi_select_count(4)),
        )
        if not uiform:
            return

        think_time()

    @task(2)
    def sustainability_filter_flow(self):
        page, uiform = self._open_sustainability()
        if not uiform:
            return

        uiform = self._apply_global_filters_if_needed(page, uiform)
        if not uiform:
            return

        uiform = page.select_product(
            uiform,
            DataEngine.sustainability_products(count=self._multi_select_count(4)),
        )
        if not uiform:
            return

        think_time()

        uiform = page.select_vehicle_type(
            uiform,
            DataEngine.vehicle_type_list(count=self._multi_select_count(4)),
        )
        if not uiform:
            return

        think_time()

        uiform = page.select_power_train(
            uiform,
            DataEngine.power_train_list(count=self._multi_select_count(4)),
        )
        if not uiform:
            return

        think_time()

        start_date = DataEngine.sustainability_start_date()
        uiform = page.set_start_date(
            uiform,
            start_date["year"],
            start_date["month"],
            start_date["day"],
        )
        if not uiform:
            return

        think_time()

        end_date = DataEngine.sustainability_end_date()
        uiform = page.set_end_date(
            uiform,
            end_date["year"],
            end_date["month"],
            end_date["day"],
        )
        if not uiform:
            return

        think_time()

    @task(1)
    def filter_reset_global_filters_flow(self):
        page, uiform = self._open_alerts()
        if not uiform:
            return

        uiform = page.reset_global_filters(uiform, self.filter_state)
        if not uiform:
            return

        think_time()

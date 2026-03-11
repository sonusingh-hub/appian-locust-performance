from locust import task

from journeys.base_journey import BaseJourney
from utils.waits import think_time
from data.data_engine import DataEngine
from pages.vehicle_on_order_page import VehicleOnOrderPage


class VehicleOnOrderJourney(BaseJourney):

    @task
    def vehicle_on_order_flow(self):
        page = VehicleOnOrderPage(self)

        uiform = page.open()
        if not uiform:
            return

        think_time()

        uiform = page.select_product(
            uiform,
            DataEngine.vehicle_on_order_products()
        )

        think_time()

        uiform = page.select_vehicle_type(
            uiform,
            DataEngine.vehicle_on_order_vehicle_types()
        )

        think_time()

        uiform = page.select_power_train(
            uiform,
            DataEngine.power_train_list()
        )

        think_time()

        uiform = page.select_expected_delivery(
            uiform,
            DataEngine.expected_delivery()
        )

        think_time()

        uiform = page.export_report(uiform)

        think_time()

        uiform = page.search_record(
            uiform,
            "Nestle"
        )

        think_time()

        uiform = page.click_search_box(uiform)

        think_time()

        uiform = page.refresh_grid(uiform)

        think_time()
from locust import task

from journeys.base_journey import BaseJourney
from utils.waits import think_time
from data.data_engine import DataEngine
from pages.sustainability_page import SustainabilityPage


class SustainabilityJourney(BaseJourney):

    @task
    def sustainability_flow(self):
        page = SustainabilityPage(self)

        uiform = page.open()
        if not uiform:
            return

        think_time()

        uiform = page.select_product(
            uiform,
            DataEngine.sustainability_products()
        )

        think_time()

        uiform = page.select_vehicle_type(
            uiform,
            DataEngine.vehicle_type_list()
        )

        think_time()

        uiform = page.select_power_train(
            uiform,
            DataEngine.power_train_list()
        )

        think_time()

        start_date = DataEngine.sustainability_start_date()
        uiform = page.set_start_date(
            uiform,
            start_date["year"],
            start_date["month"],
            start_date["day"]
        )

        think_time()

        end_date = DataEngine.sustainability_end_date()
        uiform = page.set_end_date(
            uiform,
            end_date["year"],
            end_date["month"],
            end_date["day"]
        )

        think_time()

        uiform = page.clear_filters(uiform)

        think_time()
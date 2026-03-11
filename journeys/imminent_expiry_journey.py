from locust import task

from journeys.base_journey import BaseJourney
from utils.waits import think_time
from data.data_engine import DataEngine
from pages.imminent_expiry_page import ImminentExpiryPage


class ImminentExpiryJourney(BaseJourney):

    @task
    def imminent_expiry_flow(self):
        page = ImminentExpiryPage(self)

        uiform = page.open()
        if not uiform:
            return

        think_time()

        uiform = page.select_month(
            uiform,
            DataEngine.imminent_expiry_month()
            if hasattr(DataEngine, "imminent_expiry_month")
            else DataEngine.month()
        )

        think_time()

        uiform = page.select_product(
            uiform,
            DataEngine.imminent_expiry_products()
        )

        think_time()

        uiform = page.select_vehicle_type(
            uiform,
            DataEngine.vehicle_type_list()
        )

        think_time()

        uiform = page.select_imminent_expiry(
            uiform,
            DataEngine.imminent_expiry()
        )

        think_time()

        uiform = page.select_power_train(
            uiform,
            DataEngine.power_train_list()
        )

        think_time()

        uiform = page.refresh_grid(uiform)

        think_time()

        uiform = page.export_report(uiform)

        think_time()
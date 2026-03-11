from locust import task

from journeys.base_journey import BaseJourney
from utils.waits import think_time
from data.data_engine import DataEngine
from pages.vehicle_utilisation_page import VehicleUtilisationPage


class VehicleUtilisationJourney(BaseJourney):

    @task
    def vehicle_utilisation_flow(self):
        page = VehicleUtilisationPage(self)

        uiform = page.open()
        if not uiform:
            return

        think_time()

        uiform = page.select_month(
            uiform,
            DataEngine.vehicle_utilisation_month()
            if hasattr(DataEngine, "vehicle_utilisation_month")
            else DataEngine.month()
        )

        think_time()

        uiform = page.select_product(
            uiform,
            DataEngine.vehicle_utilisation_products()
        )

        think_time()

        uiform = page.select_vehicle_type(
            uiform,
            DataEngine.vehicle_type_list()
        )

        think_time()

        uiform = page.select_imminent_expiry(
            uiform,
            "Next 30 Days"
        )

        think_time()

        uiform = page.select_power_train(
            uiform,
            DataEngine.power_train_list()
        )

        think_time()

        uiform = page.export_report(uiform)

        think_time()

        uiform = page.refresh_grid(uiform)

        think_time()
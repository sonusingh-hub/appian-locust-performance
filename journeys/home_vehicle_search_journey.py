from locust import task

from journeys.base_journey import BaseJourney
from utils.waits import think_time
from data.data_engine import DataEngine
from pages.home_page import HomePage


class HomeVehicleSearchJourney(BaseJourney):

    @task
    def home_vehicle_search_flow(self):
        home = HomePage(self)

        uiform = home.open()
        if not uiform:
            return

        think_time()

        uiform = home.open_vehicle_search(uiform)
        if not uiform:
            return

        think_time()

        uiform = home.select_country(
            uiform,
            "Australia"
        )

        think_time()

        uiform = home.fill_registration(
            uiform,
            DataEngine.registration()
        )

        think_time()
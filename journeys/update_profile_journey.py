from locust import task

from journeys.base_journey import BaseJourney
from utils.waits import think_time
from data.data_engine import DataEngine
from pages.update_profile_page import UpdateProfilePage


class UpdateProfileJourney(BaseJourney):

    @task
    def update_profile_flow(self):
        page = UpdateProfilePage(self)

        uiform = page.open()
        if not uiform:
            return

        think_time()

        uiform = page.select_language(
            uiform,
            DataEngine.language()
        )

        think_time()
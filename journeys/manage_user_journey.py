from locust import task

from journeys.base_journey import BaseJourney
from utils.waits import think_time
from data.data_engine import DataEngine
from pages.manage_user_page import ManageUserPage


class ManageUserJourney(BaseJourney):

    @task
    def manage_user_flow(self):
        page = ManageUserPage(self)

        uiform = page.open()
        if not uiform:
            return

        think_time()

        uiform = page.search_record(
            uiform,
            DataEngine.manage_user_search()
        )

        think_time()

        uiform = page.click_search_box(uiform)

        think_time()

        uiform = page.filter_user_group(
            uiform,
            DataEngine.manage_user_filters()
        )

        think_time()

        uiform = page.export_report(uiform)

        think_time()

        uiform = page.clear_filters(uiform)

        think_time()
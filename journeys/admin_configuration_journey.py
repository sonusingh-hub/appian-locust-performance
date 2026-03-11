from locust import task

from journeys.base_journey import BaseJourney
from utils.waits import think_time
from pages.admin_configuration_page import AdminConfigurationPage


class AdminConfigurationJourney(BaseJourney):

    @task
    def admin_configuration_flow(self):
        page = AdminConfigurationPage(self)

        uiform = page.open()
        if not uiform:
            return

        think_time()

        uiform = page.open_industry_trends(uiform)
        if not uiform:
            return

        think_time()

        uiform = page.cancel(uiform)
        if not uiform:
            return

        think_time()

        uiform = page.refresh_after_update(uiform)

        think_time()
from locust import task

from journeys.base_journey import BaseJourney
from utils.waits import think_time
from pages.admin_configuration_page import AdminConfigurationPage


class AdminConfigurationJourney(BaseJourney):
    journey_name = "admin_configuration"

    @task
    def admin_configuration_recorded_flow(self):
        page = AdminConfigurationPage(self)

        uiform = page.open()
        if not uiform:
            return

        think_time()

        uiform = page.open_industry_trends(uiform)
        if not uiform:
            return

        think_time()

        uiform = page.cancel_action_dialog(uiform)
        if not uiform:
            return

        think_time()

        uiform = page.refresh_after_action(uiform)
        if not uiform:
            return

        think_time()

        uiform = page.open_manage(uiform)
        if not uiform:
            return

        think_time()

        uiform = page.cancel_action_dialog(uiform)
        if not uiform:
            return

        think_time()

        uiform = page.refresh_after_action(uiform)
        if not uiform:
            return

        think_time()

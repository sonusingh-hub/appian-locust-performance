from locust import task

from journeys.base_journey import BaseJourney
from utils.waits import think_time
from pages.manage_user_page import ManageUserPage


class ManageUserJourney(BaseJourney):
    journey_name = "manage_user"

    SEARCH_VALUE = "Johnson"

    USER_GROUP_SEQUENCE = [
        ["Nestle"],
        ["Nestle", "Colgate"],
        ["Nestle", "Colgate", "Johnson & Johnson"],
        ["Nestle", "Colgate", "Johnson & Johnson", "AstraZeneca"],
        [],
    ]

    @task
    def manage_user_recorded_flow(self):
        page = ManageUserPage(self)

        uiform = page.open()
        if not uiform:
            return

        think_time()

        uiform = page.search_record(uiform, self.SEARCH_VALUE)
        if not uiform:
            return

        think_time()

        uiform = page.click_search_box(uiform)
        if not uiform:
            return

        think_time()

        uiform = page.clear_search(uiform)
        if not uiform:
            return

        think_time()

        for groups in self.USER_GROUP_SEQUENCE:
            uiform = page.apply_user_groups(uiform, groups)
            if not uiform:
                return

            think_time()

        uiform = page.export_grid(uiform)
        if not uiform:
            return

        think_time()

        uiform = page.refresh_grid(uiform)
        if not uiform:
            return

        think_time()

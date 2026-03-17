from locust import task

from journeys.base_journey import BaseJourney
from utils.waits import think_time
from pages.update_profile_page import UpdateProfilePage


class UpdateProfileJourney(BaseJourney):
    journey_name = "update_profile"

    LANGUAGE_SEQUENCE = [
        "English(UK) [en_GB]",
        "English(US) [en_US]",
        "Thai [th]",
        "English(Australia) [en_AU]",
        "English(UK) [en_GB]",
    ]
    TIME_ZONE_SEQUENCE = [
        "(UTC+10:00) Australian Eastern Standard Time (Australia/Brisbane)",
        "(UTC+10:00) Eastern Australia Time (Australia/Sydney)",
    ]

    @task
    def update_profile_flow(self):
        page = UpdateProfilePage(self)

        uiform = page.open()
        if not uiform:
            return

        think_time()

        for language in self.LANGUAGE_SEQUENCE:
            uiform = page.select_language(uiform, language)
            if not uiform:
                return

            think_time()

        for time_zone in self.TIME_ZONE_SEQUENCE:
            uiform = page.select_time_zone(uiform, time_zone)
            if not uiform:
                return

            think_time()
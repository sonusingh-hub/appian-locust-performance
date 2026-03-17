from appian_locust import AppianTaskSet

from core.global_filters_state import GlobalFiltersState


class BaseJourney(AppianTaskSet):

    journey_name = "base"

    def on_start(self):
        super().on_start()

        if not hasattr(self, "user_context"):
            self.user_context = {}

        self.user_context["journey_name"] = self.journey_name

        # Per-VUser tracker for the four global report filters.
        # All report-page journeys can read / write this to avoid re-applying
        # filters that Appian already persists server-side for the session.
        self.filter_state = GlobalFiltersState()
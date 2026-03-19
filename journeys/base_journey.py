import random

from appian_locust import AppianTaskSet

from core.global_filters_state import GlobalFiltersState
from utils.waits import abandonment_enabled


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

    def _get_page_filter_values(self, page_key, builder):
        cache = self.user_context.setdefault("page_filter_values", {})
        if page_key not in cache:
            cache[page_key] = builder()
        return cache[page_key]

    def _clear_page_filter_values(self, *page_keys):
        cache = self.user_context.setdefault("page_filter_values", {})
        if not page_keys:
            cache.clear()
            return

        for page_key in page_keys:
            cache.pop(page_key, None)

    def _should_abandon(self, probability=0.05):
        """Return True with the given probability to simulate a user navigating
        away mid-journey (e.g. clicking a notification, switching tabs).
        Call at natural pause points in a flow; return early when True."""
        if not abandonment_enabled():
            return False
        return random.random() < probability
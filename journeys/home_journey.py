from locust import task

from journeys.base_journey import BaseJourney
from utils.waits import think_time, small_wait
from data.data_engine import DataEngine
from pages.home_page import HomePage


class HomeJourney(BaseJourney):
    journey_name = "home"

    def _open_home(self):
        page = HomePage(self)

        uiform = page.open()
        if not uiform:
            return page, None

        think_time()
        small_wait()
        return page, uiform

    def _apply_base_home_filters(self, page, uiform):
        """Apply global filters, reusing already-selected values when possible.

        Appian persists filters server-side across page navigations, so we only
        need to call apply_global_filters() when the state says filters are not
        currently in effect (e.g. after a reset or at the start of a new session).
        """
        if self.filter_state.is_applied:
            return uiform

        uiform = page.apply_global_filters(
            uiform,
            self.filter_state,
            countries=DataEngine.home_country_list(),
        )
        if not uiform:
            return None

        think_time()
        return uiform

    @task(4)
    def home_country_flow(self):
        page, uiform = self._open_home()
        if not uiform:
            return

        uiform = self._apply_base_home_filters(page, uiform)
        if not uiform:
            return

    @task(3)
    def home_client_filters_flow(self):
        """Apply all four global filters in cascade order."""
        page, uiform = self._open_home()
        if not uiform:
            return

        # Country must be set before Client Group choices are populated.
        uiform = page.apply_global_filters(
            uiform,
            self.filter_state,
            countries=DataEngine.home_country_list(),
            client_groups=DataEngine.home_client_groups(),
            client_names=DataEngine.home_client_names(),
            bill_to_values=DataEngine.home_bill_to(),
        )
        if not uiform:
            return

        think_time()

    @task(1)
    def home_reset_filters_flow(self):
        page, uiform = self._open_home()
        if not uiform:
            return

        # reset_global_filters clears self.filter_state so the next task
        # will re-apply filters from scratch.
        uiform = page.reset_global_filters(uiform, self.filter_state)
        if not uiform:
            return

        think_time()
from locust import task

from journeys.base_journey import BaseJourney
from utils.waits import think_time, small_wait
from data.data_engine import DataEngine
from pages.alerts_page import AlertsPage


class AlertsJourney(BaseJourney):
    journey_name = "alerts"

    def _open_alerts(self):
        alerts = AlertsPage(self)

        uiform = alerts.open()
        if not uiform:
            return alerts, None

        think_time()
        small_wait()
        return alerts, uiform

    def _return_to_alerts(self, alerts):
        """Return to Alerts with deterministic navigation.

        Keeps each task ending on a known page state and avoids reliance on
        fragile in-page back interactions when card details are opened.
        """
        uiform = alerts.open()
        if not uiform:
            return None

        think_time()
        small_wait()
        return uiform

    def _open_alert_card_flow(self, open_card_action):
        alerts, uiform = self._open_alerts()
        if not uiform:
            return

        uiform = open_card_action(alerts, uiform)
        if not uiform:
            return

        think_time()

        uiform = self._return_to_alerts(alerts)
        if not uiform:
            return

        think_time()

    @task(5)
    def alerts_search_flow(self):
        alerts, uiform = self._open_alerts()
        if not uiform:
            return

        uiform = alerts.search_record(
            uiform,
            DataEngine.company()
        )
        if not uiform:
            return

        think_time()

        uiform = alerts.click_search_box(uiform)
        if not uiform:
            return

        think_time()

    @task(3)
    def alerts_refresh_flow(self):
        alerts, uiform = self._open_alerts()
        if not uiform:
            return

        uiform = alerts.refresh_grid(uiform)
        if not uiform:
            return

        think_time()

    @task(1)
    def alerts_filter_flow(self):
        alerts, uiform = self._open_alerts()
        if not uiform:
            return

        uiform = alerts.filter_country(
            uiform,
            DataEngine.country()
        )
        if not uiform:
            return

        think_time()

        uiform = alerts.reset_filters(uiform, self.filter_state)
        if not uiform:
            return

        think_time()

    @task(2)
    def alerts_paging_flow(self):
        alerts, uiform = self._open_alerts()
        if not uiform:
            return

        uiform = alerts.move_grid_right_multiple(uiform, count=3, index=0)
        if not uiform:
            return

        think_time()

        uiform = alerts.move_grid_to_end(uiform, index=0)
        if not uiform:
            return

        think_time()

        uiform = alerts.move_grid_to_beginning(uiform, index=0)
        if not uiform:
            return

        think_time()

    @task(1)
    def alerts_vehicle_overdue_registration_flow(self):
        self._open_alert_card_flow(
            lambda alerts, uiform: alerts.open_vehicles_overdue_registration(uiform)
        )

    @task(1)
    def alerts_vehicle_overdue_servicing_flow(self):
        self._open_alert_card_flow(
            lambda alerts, uiform: alerts.open_vehicles_overdue_servicing(uiform)
        )

    @task(1)
    def alerts_vehicle_utilisation_threshold_flow(self):
        self._open_alert_card_flow(
            lambda alerts, uiform: alerts.open_vehicle_utilisation_threshold(uiform)
        )

    @task(1)
    def alerts_vehicle_contracts_expired_flow(self):
        self._open_alert_card_flow(
            lambda alerts, uiform: alerts.open_vehicle_contracts_expired(uiform)
        )

    @task(1)
    def alerts_vehicle_contracts_due_off_flow(self):
        self._open_alert_card_flow(
            lambda alerts, uiform: alerts.open_vehicle_contracts_due_off(uiform)
        )

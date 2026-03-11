from locust import task
import random

from journeys.base_journey import BaseJourney
from utils.waits import think_time
from data.data_engine import DataEngine
from pages.home_page import HomePage
from pages.alerts_page import AlertsPage
from pages.fleet_schedule_page import FleetSchedulePage
from pages.vehicle_on_order_page import VehicleOnOrderPage


class FilterJourney(BaseJourney):

    @task
    def filter_flow(self):
        home = HomePage(self)

        uiform = home.open()
        if not uiform:
            return

        think_time()

        uiform = home.select_country(
            uiform,
            DataEngine.country()
        )

        think_time()

        flow = random.choice([
            "alerts",
            "fleet_schedule",
            "vehicle_on_order"
        ])

        if flow == "alerts":
            alerts = AlertsPage(self)

            uiform = alerts.open()
            if not uiform:
                return

            think_time()

            uiform = alerts.search_record(
                uiform,
                DataEngine.company()
            )

            think_time()

            uiform = alerts.click_search_box(uiform)

            think_time()

            uiform = alerts.filter_country(
                uiform,
                DataEngine.country()
            )

            think_time()

        elif flow == "fleet_schedule":
            fleet = FleetSchedulePage(self)

            uiform = fleet.open()
            if not uiform:
                return

            think_time()

            uiform = fleet.select_product(
                uiform,
                DataEngine.fleet_schedule_products()
            )

            think_time()

            uiform = fleet.select_vehicle_type(
                uiform,
                DataEngine.vehicle_type_list()
            )

            think_time()

            uiform = fleet.select_imminent_expiry(
                uiform,
                DataEngine.imminent_expiry()
            )

            think_time()

            uiform = fleet.select_power_train(
                uiform,
                DataEngine.power_train_list()
            )

            think_time()

        else:
            voo = VehicleOnOrderPage(self)

            uiform = voo.open()
            if not uiform:
                return

            think_time()

            uiform = voo.select_product(
                uiform,
                DataEngine.vehicle_on_order_products()
            )

            think_time()

            uiform = voo.select_vehicle_type(
                uiform,
                DataEngine.vehicle_on_order_vehicle_types()
            )

            think_time()

            uiform = voo.select_power_train(
                uiform,
                DataEngine.power_train_list()
            )

            think_time()

            uiform = voo.select_expected_delivery(
                uiform,
                DataEngine.expected_delivery()
            )

            think_time()

        home.open()
        think_time()
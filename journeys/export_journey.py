from locust import task
import random

from journeys.base_journey import BaseJourney
from utils.waits import think_time
from data.data_engine import DataEngine
from pages.alerts_page import AlertsPage
from pages.fleet_schedule_page import FleetSchedulePage
from pages.vehicle_on_order_page import VehicleOnOrderPage


class ExportJourney(BaseJourney):

    @task
    def export_flow(self):
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

            uiform = alerts.filter_country(
                uiform,
                DataEngine.country()
            )

            think_time()

            uiform = alerts.export_report(uiform)

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

            uiform = fleet.export_report(uiform)

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

            uiform = voo.export_report(uiform)

            think_time()
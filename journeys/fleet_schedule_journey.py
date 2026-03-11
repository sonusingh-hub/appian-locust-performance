from locust import task

from journeys.base_journey import BaseJourney
from utils.waits import think_time
from data.data_engine import DataEngine
from pages.fleet_schedule_page import FleetSchedulePage


class FleetScheduleJourney(BaseJourney):

    @task
    def fleet_schedule_flow(self):
        page = FleetSchedulePage(self)

        uiform = page.open()
        if not uiform:
            return

        think_time()

        uiform = page.select_product(
            uiform,
            DataEngine.fleet_schedule_products()
        )

        think_time()

        uiform = page.select_vehicle_type(
            uiform,
            DataEngine.vehicle_type_list()
        )

        think_time()

        uiform = page.select_imminent_expiry(
            uiform,
            DataEngine.imminent_expiry()
        )

        think_time()

        uiform = page.select_power_train(
            uiform,
            DataEngine.power_train_list()
        )

        think_time()

        uiform = page.show_account_filters(uiform)

        think_time()

        uiform = page.select_country(
            uiform,
            DataEngine.country_list() if hasattr(DataEngine, "country_list") else [DataEngine.country()]
        )

        think_time()

        uiform = page.select_client_group(
            uiform,
            DataEngine.fleet_schedule_client_groups()
        )

        think_time()

        uiform = page.select_client_name(
            uiform,
            DataEngine.fleet_schedule_client_names()
        )

        think_time()

        uiform = page.select_bill_to(
            uiform,
            DataEngine.fleet_schedule_bill_to()
        )

        think_time()

        uiform = page.export_report(uiform)

        think_time()

        uiform = page.search_record(
            uiform,
            DataEngine.company()
        )

        think_time()

        uiform = page.click_search_box(uiform)

        think_time()
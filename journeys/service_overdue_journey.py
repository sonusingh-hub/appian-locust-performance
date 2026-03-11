from locust import task

from journeys.base_journey import BaseJourney
from utils.waits import think_time
from data.data_engine import DataEngine
from pages.service_overdue_page import ServiceOverduePage


class ServiceOverdueJourney(BaseJourney):

    @task
    def service_overdue_flow(self):
        page = ServiceOverduePage(self)

        uiform = page.open()
        if not uiform:
            return

        think_time()

        uiform = page.select_product(
            uiform,
            DataEngine.service_overdue_products()
        )

        think_time()

        uiform = page.select_month(
            uiform,
            DataEngine.service_overdue_month()
            if hasattr(DataEngine, "service_overdue_month")
            else DataEngine.month()
        )

        think_time()

        uiform = page.select_overdue_by(
            uiform,
            DataEngine.overdue_by()
        )

        think_time()

        uiform = page.select_vehicle_type(
            uiform,
            DataEngine.vehicle_type_list()
        )

        think_time()

        uiform = page.select_power_train(
            uiform,
            DataEngine.power_train_list()
        )

        think_time()

        uiform = page.select_maintenance_included(
            uiform,
            DataEngine.maintenance_included()
        )

        think_time()

        uiform = page.export_report(uiform)

        think_time()
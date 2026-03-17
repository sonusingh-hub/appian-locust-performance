from pages.reports_navigation_page import ReportsNavigationPage
from core.ui_helpers import (
    select_multi_dropdown,
    fill_date_field,
)


class SustainabilityPage(ReportsNavigationPage):

    def open(self):
        uiform = self.open_reports()
        if not uiform:
            return None

        return self.open_sustainability(uiform)

    def select_product(self, uiform, products):
        if not uiform:
            return None

        return select_multi_dropdown(
            uiform,
            "Product",
            products,
        )

    def select_vehicle_type(self, uiform, vehicle_types):
        if not uiform:
            return None

        return select_multi_dropdown(
            uiform,
            "Vehicle Type",
            vehicle_types,
        )

    def select_power_train(self, uiform, power_trains):
        if not uiform:
            return None

        return select_multi_dropdown(
            uiform,
            "Power Train",
            power_trains,
        )

    def set_start_date(self, uiform, year, month, day):
        if not uiform:
            return None

        return fill_date_field(
            uiform,
            label="Start date",
            year=year,
            month=month,
            day=day,
        )

    def set_end_date(self, uiform, year, month, day):
        if not uiform:
            return None

        return fill_date_field(
            uiform,
            label="End date",
            year=year,
            month=month,
            day=day,
        )

from datetime import date

from core.base_page import BasePage
from core.ui_helpers import select_multi_dropdown, click_button
from utils.waits import small_wait


class SustainabilityPage(BasePage):

    def open(self):
        return self.visit(
            site_name="apac-reporting",
            page_name="sustainability"
        )

    def select_product(self, uiform, products):
        if not uiform:
            return None

        return select_multi_dropdown(
            uiform,
            "Product",
            products
        )

    def select_vehicle_type(self, uiform, vehicle_types):
        if not uiform:
            return None

        return select_multi_dropdown(
            uiform,
            "Vehicle Type",
            vehicle_types
        )

    def select_power_train(self, uiform, power_trains):
        if not uiform:
            return None

        return select_multi_dropdown(
            uiform,
            "Power Train",
            power_trains
        )

    def set_start_date(self, uiform, year, month, day):
        if not uiform:
            return None

        uiform.fill_date_field(
            label="Start date",
            date_input=date(year=year, month=month, day=day)
        )
        small_wait()
        return uiform

    def set_end_date(self, uiform, year, month, day):
        if not uiform:
            return None

        uiform.fill_date_field(
            label="End date",
            date_input=date(year=year, month=month, day=day)
        )
        small_wait()
        return uiform

    def clear_filters(self, uiform):
        if not uiform:
            return None

        return click_button(
            uiform,
            "Clear Filters"
        )
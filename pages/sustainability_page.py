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

        if self.page_filter_state.is_filter_set("product", products):
            return uiform

        result = select_multi_dropdown(
            uiform,
            "Product",
            products,
        )
        if result:
            self.page_filter_state.set_filter("product", products)
        return result

    def select_vehicle_type(self, uiform, vehicle_types):
        if not uiform:
            return None

        if self.page_filter_state.is_filter_set("vehicle_type", vehicle_types):
            return uiform

        result = select_multi_dropdown(
            uiform,
            "Vehicle Type",
            vehicle_types,
        )
        if result:
            self.page_filter_state.set_filter("vehicle_type", vehicle_types)
        return result

    def select_power_train(self, uiform, power_trains):
        if not uiform:
            return None

        if self.page_filter_state.is_filter_set("power_train", power_trains):
            return uiform

        result = select_multi_dropdown(
            uiform,
            "Power Train",
            power_trains,
        )
        if result:
            self.page_filter_state.set_filter("power_train", power_trains)
        return result

    def set_start_date(self, uiform, year, month, day):
        if not uiform:
            return None

        date_value = (year, month, day)
        if self.page_filter_state.is_filter_set("start_date", date_value):
            return uiform

        result = fill_date_field(
            uiform,
            label="Start date",
            year=year,
            month=month,
            day=day,
        )
        if result:
            self.page_filter_state.set_filter("start_date", date_value)
        return result

    def set_end_date(self, uiform, year, month, day):
        if not uiform:
            return None

        date_value = (year, month, day)
        if self.page_filter_state.is_filter_set("end_date", date_value):
            return uiform

        result = fill_date_field(
            uiform,
            label="End date",
            year=year,
            month=month,
            day=day,
        )
        if result:
            self.page_filter_state.set_filter("end_date", date_value)
        return result

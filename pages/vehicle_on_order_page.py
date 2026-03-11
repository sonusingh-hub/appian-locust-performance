from core.base_page import BasePage
from core.ui_helpers import select_dropdown, select_multi_dropdown, click_button


class VehicleOnOrderPage(BasePage):

    def open(self):
        return self.visit(
            site_name="apac-reporting",
            page_name="vehicle-on-order"
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

    def select_expected_delivery(self, uiform, value):
        if not uiform:
            return None

        return select_dropdown(
            uiform,
            "Expected Delivery",
            value
        )

    def export_report(self, uiform):
        if not uiform:
            return None

        return click_button(
            uiform,
            "gridField_recordData_dataExportButton",
            True
        )

    def search_record(self, uiform, value):
        if not uiform:
            return None

        uiform.fill_text_field(
            label="recordSearchBox",
            value=value,
            is_test_label=True
        )
        return uiform

    def click_search_box(self, uiform):
        if not uiform:
            return None

        uiform.click(
            label="recordSearchBox",
            is_test_label=True
        )
        return uiform

    def refresh_grid(self, uiform):
        if not uiform:
            return None

        return click_button(
            uiform,
            "gridField_recordData_refreshButton",
            True
        )
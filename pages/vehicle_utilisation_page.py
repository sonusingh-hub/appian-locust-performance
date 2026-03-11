from core.base_page import BasePage
from core.ui_helpers import select_dropdown, select_multi_dropdown, click_button


class VehicleUtilisationPage(BasePage):

    def open(self):
        return self.visit(
            site_name="apac-reporting",
            page_name="vehicle-utilisation"
        )

    def select_month(self, uiform, month):
        if not uiform:
            return None

        return select_dropdown(
            uiform,
            "Month",
            month
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

    def select_imminent_expiry(self, uiform, value):
        if not uiform:
            return None

        return select_dropdown(
            uiform,
            "Imminent Expiry",
            value
        )

    def select_power_train(self, uiform, power_trains):
        if not uiform:
            return None

        return select_multi_dropdown(
            uiform,
            "Power Train",
            power_trains
        )

    def search_record(self, uiform, value):
        if not uiform:
            return None

        new_uiform = uiform.fill_text_field(
            label="Vehicle Utilisation-recordSearchBox",
            value=value,
            is_test_label=True
        )
        return new_uiform

    def click_search_box(self, uiform):
        if not uiform:
            return None

        new_uiform = uiform.click(
            label="Vehicle Utilisation-recordSearchBox",
            is_test_label=True
        )
        return new_uiform

    def refresh_grid(self, uiform):
        if not uiform:
            return None

        return click_button(
            uiform,
            "gridField_recordData_refreshButton",
            True
        )

    def export_report(self, uiform):
        if not uiform:
            return None

        return click_button(
            uiform,
            "gridField_recordData_dataExportButton",
            True
        )
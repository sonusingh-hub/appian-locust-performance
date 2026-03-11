from core.base_page import BasePage
from core.ui_helpers import select_dropdown, select_multi_dropdown, click_button


class FleetSchedulePage(BasePage):

    def open(self):
        return self.visit(
            site_name="apac-reporting",
            page_name="fleet-schedule"
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

    def show_account_filters(self, uiform):
        if not uiform:
            return None

        return click_button(
            uiform,
            "Show Account Filters"
        )

    def select_country(self, uiform, countries):
        if not uiform:
            return None

        return select_multi_dropdown(
            uiform,
            "Country",
            countries
        )

    def select_client_group(self, uiform, client_groups):
        if not uiform:
            return None

        return select_multi_dropdown(
            uiform,
            "Client Group",
            client_groups
        )

    def select_client_name(self, uiform, client_names):
        if not uiform:
            return None

        return select_multi_dropdown(
            uiform,
            "Client Name",
            client_names
        )

    def select_bill_to(self, uiform, bill_to_values):
        if not uiform:
            return None

        return select_multi_dropdown(
            uiform,
            "Bill To",
            bill_to_values
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
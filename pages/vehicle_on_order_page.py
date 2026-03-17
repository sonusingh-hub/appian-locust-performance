from pages.reports_navigation_page import ReportsNavigationPage
from core.ui_helpers import (
    select_dropdown,
    select_multi_dropdown,
    click_button,
    fill_text_field,
    click_field,
    click_card_by_text,
    click_clickable_by_text,
    has_component_label,
    has_component_text,
)


class VehicleOnOrderPage(ReportsNavigationPage):

    CARD_TEXTS = (
        "Vehicles On Order",
        "Funded Vehicles on Order",
        "Delivery Overdue",
    )
    EXPORT_BUTTON_TEST_LABELS = (
        "gridField_recordData_dataExportButton",
        "recordData_dataExportButton",
        "dataExportButton",
    )

    def open(self):
        uiform = self.open_reports()
        if not uiform:
            return None

        return self.open_vehicle_on_order(uiform)

    def select_product(self, uiform, products):
        if not uiform:
            return None

        return select_multi_dropdown(uiform, "Product", products)

    def select_vehicle_type(self, uiform, vehicle_types):
        if not uiform:
            return None

        return select_multi_dropdown(uiform, "Vehicle Type", vehicle_types)

    def select_power_train(self, uiform, power_trains):
        if not uiform:
            return None

        return select_multi_dropdown(uiform, "Power Train", power_trains)

    def select_expected_delivery(self, uiform, option):
        if not uiform:
            return None

        return select_dropdown(uiform, "Expected Delivery", option)

    def search_record(self, uiform, value):
        if not uiform:
            return None

        return fill_text_field(
            uiform,
            label="recordSearchBox",
            value=value,
            is_test_label=True,
        )

    def click_search_box(self, uiform):
        if not uiform:
            return None

        return click_field(
            uiform,
            label="recordSearchBox",
            is_test_label=True,
        )

    def export_report(self, uiform):
        if not uiform:
            return None

        if not self._is_export_card_selected():
            return uiform

        for test_label in self.EXPORT_BUTTON_TEST_LABELS:
            if not has_component_label(uiform, test_label, is_test_label=True):
                continue

            updated = click_button(
                uiform,
                test_label,
                True,
            )
            if updated:
                return updated

        if has_component_text(uiform, "Export"):
            updated = click_clickable_by_text(uiform, "Export", timeout=3)
            if updated:
                return updated

        return uiform

    def open_vehicle_on_order_card(self, uiform, label):
        if not uiform:
            return None

        if label not in self.CARD_TEXTS:
            return None

        updated_uiform = click_card_by_text(uiform, label)
        if updated_uiform:
            self._mark_export_card_selected()
            return updated_uiform

        updated_uiform = click_clickable_by_text(uiform, label)
        if updated_uiform:
            self._mark_export_card_selected()
            return updated_uiform

        return None

    def open_vehicles_on_order(self, uiform):
        return self.open_vehicle_on_order_card(uiform, self.CARD_TEXTS[0])

    def open_funded_vehicles_on_order(self, uiform):
        return self.open_vehicle_on_order_card(uiform, self.CARD_TEXTS[1])

    def open_delivery_overdue(self, uiform):
        return self.open_vehicle_on_order_card(uiform, self.CARD_TEXTS[2])

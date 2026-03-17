from pages.reports_navigation_page import ReportsNavigationPage
from core.ui_helpers import (
    select_dropdown,
    select_multi_dropdown,
    click_button,
    click_card_by_text,
    click_clickable_by_text,
    has_component_label,
    has_component_text,
)


class VehicleUtilisationPage(ReportsNavigationPage):

    CARD_TEXTS = (
        "Active Vehicles",
        "Vehicle Utilisation",
        "Predicted Variance at Contract End",
        "Maximum Variance",
        "Minimum Variance",
    )

    DETAIL_SEARCH_LABELS = (
        "Vehicle Utilisation-recordSearchBox",
        "recordSearchBox",
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

        # Explicitly call the parent nav method because this class defines its
        # own open_vehicle_utilisation() (opens the detail card), which would
        # shadow the inherited left-nav navigation method if called via self.
        return ReportsNavigationPage.open_vehicle_utilisation(self, uiform)

    def select_month(self, uiform, month):
        """Select the Month filter.

        On some Appian builds the Month field renders as a MultipleDropdownWidget
        instead of a DropdownField, causing select_dropdown to raise
        ComponentNotFoundException.  We try the standard dropdown first and fall
        back to multi-select with a single value so both renderings work.
        """
        if not uiform:
            return None

        updated = select_dropdown(uiform, "Month", month, timeout=3)
        if updated:
            return updated

        return select_multi_dropdown(uiform, "Month", [month])

    def select_product(self, uiform, products):
        if not uiform:
            return None

        return select_multi_dropdown(uiform, "Product", products)

    def select_vehicle_type(self, uiform, vehicle_types):
        if not uiform:
            return None

        return select_multi_dropdown(uiform, "Vehicle Type", vehicle_types)

    def select_imminent_expiry(self, uiform, option):
        if not uiform:
            return None

        return select_dropdown(uiform, "Imminent Expiry", option)

    def select_power_train(self, uiform, power_trains):
        if not uiform:
            return None

        return select_multi_dropdown(uiform, "Power Train", power_trains)

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

    def search_detail_record(self, uiform, value):
        return self.fill_report_search(uiform, value, self.DETAIL_SEARCH_LABELS)

    def click_detail_search_box(self, uiform):
        return self.click_report_search_box(uiform, self.DETAIL_SEARCH_LABELS)

    def open_vehicle_utilisation_card(self, uiform, label):
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

    def open_active_vehicles(self, uiform):
        return self.open_vehicle_utilisation_card(uiform, self.CARD_TEXTS[0])

    def open_vehicle_utilisation(self, uiform):
        return self.open_vehicle_utilisation_card(uiform, self.CARD_TEXTS[1])

    def open_predicted_variance(self, uiform):
        return self.open_vehicle_utilisation_card(uiform, self.CARD_TEXTS[2])

    def open_maximum_variance(self, uiform):
        return self.open_vehicle_utilisation_card(uiform, self.CARD_TEXTS[3])

    def open_minimum_variance(self, uiform):
        return self.open_vehicle_utilisation_card(uiform, self.CARD_TEXTS[4])

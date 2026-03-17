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


class ImminentExpiryPage(ReportsNavigationPage):

    CARD_TEXTS = (
        "Imminent Expiry",
        "Vehicle Utilisation",
    )

    DETAIL_SEARCH_LABELS = (
        "Imminent Expiry Grid-recordSearchBox",
        "Imminent Contract Expiry-recordSearchBox",
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

        return self.open_imminent_expiry(uiform)

    def select_month(self, uiform, month):
        """Select the Month filter.

        Falls back to multi-select when the Month field is a
        MultipleDropdownWidget rather than a DropdownField.
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

    def open_imminent_expiry_card(self, uiform):
        if not uiform:
            return None

        updated_uiform = click_card_by_text(uiform, self.CARD_TEXTS[0])
        if updated_uiform:
            self._mark_export_card_selected()
            return updated_uiform

        updated_uiform = click_clickable_by_text(uiform, self.CARD_TEXTS[0])
        if updated_uiform:
            self._mark_export_card_selected()
            return updated_uiform

        return None

    def open_vehicle_utilisation_card(self, uiform):
        if not uiform:
            return None

        updated_uiform = click_card_by_text(uiform, self.CARD_TEXTS[1])
        if updated_uiform:
            self._mark_export_card_selected()
            return updated_uiform

        updated_uiform = click_clickable_by_text(uiform, self.CARD_TEXTS[1])
        if updated_uiform:
            self._mark_export_card_selected()
            return updated_uiform

        return None

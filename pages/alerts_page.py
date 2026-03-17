from pages.reports_navigation_page import ReportsNavigationPage
from core.ui_helpers import (
    click_button,
    click_card_by_text,
    click_clickable_by_text,
    has_component_label,
    has_component_text,
)


class AlertsPage(ReportsNavigationPage):

    SEARCH_BOX_TEST_LABELS = (
        "recordSearchBox",
        "Alerts-recordSearchBox",
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

        return self.open_alerts(uiform)

    def search_record(self, uiform, value):
        return self.fill_report_search(uiform, value, self.SEARCH_BOX_TEST_LABELS)

    def click_search_box(self, uiform):
        return self.click_report_search_box(uiform, self.SEARCH_BOX_TEST_LABELS)

    def refresh_grid(self, uiform):
        if not uiform:
            return None

        return click_button(
            uiform,
            "gridField_recordData_refreshButton",
            True
        )

    def clear_filters(self, uiform, timeout=10):
        if not uiform:
            return None

        return click_button(
            uiform,
            "Clear Filters Option",
            timeout=timeout
        )

    def reset_filters(self, uiform, filter_state=None):
        """Alias for reset_global_filters so existing journey code still works."""
        return self.reset_global_filters(uiform, filter_state)

    def filter_country(self, uiform, country):
        """Select Country filter.  Delegates to the shared select_country() helper."""
        return self.select_country(uiform, country)

    def move_grid_right(self, uiform, index=0):
        if not uiform:
            return None

        return uiform.move_to_right_in_paging_grid(index=index)

    def move_grid_right_multiple(self, uiform, count=1, index=0):
        if not uiform:
            return None

        current_uiform = uiform

        for _ in range(count):
            if not current_uiform:
                return None

            current_uiform = current_uiform.move_to_right_in_paging_grid(index=index)

        return current_uiform

    def move_grid_to_end(self, uiform, index=0):
        if not uiform:
            return None

        return uiform.move_to_end_of_paging_grid(index=index)

    def move_grid_to_beginning(self, uiform, index=0):
        if not uiform:
            return None

        return uiform.move_to_beginning_of_paging_grid(index=index)

    def export_report(self, uiform):
        if not uiform:
            return None

        for test_label in self.EXPORT_BUTTON_TEST_LABELS:
            if not has_component_label(uiform, test_label, is_test_label=True):
                continue

            updated = click_button(
                uiform,
                test_label,
                True
            )
            if updated:
                return updated

        if has_component_text(uiform, "Export"):
            updated = click_clickable_by_text(uiform, "Export", timeout=3)
            if updated:
                return updated

        return uiform

    def open_alert_card(self, uiform, label):
        if not uiform:
            return None

        updated_uiform = click_card_by_text(uiform, label)
        if updated_uiform:
            return updated_uiform

        return click_clickable_by_text(uiform, label)

    def open_vehicles_overdue_registration(self, uiform):
        if not uiform:
            return None

        return self.open_alert_card(
            uiform,
            "Vehicles Overdue for registration"
        )

    def open_vehicles_overdue_servicing(self, uiform):
        if not uiform:
            return None

        return self.open_alert_card(
            uiform,
            "Vehicles Overdue for servicing"
        )

    def open_vehicle_utilisation_threshold(self, uiform):
        if not uiform:
            return None

        return self.open_alert_card(
            uiform,
            "Vehicle Utilisation"
        )

    def open_vehicle_contracts_expired(self, uiform):
        if not uiform:
            return None

        return self.open_alert_card(
            uiform,
            "Vehicle Contracts already expired"
        )

    def open_vehicle_contracts_due_off(self, uiform):
        if not uiform:
            return None

        return self.open_alert_card(
            uiform,
            "Vehicle Contracts Due Off in the next 30 days"
        )

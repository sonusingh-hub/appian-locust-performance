from core.base_page import BasePage
from core.ui_helpers import select_dropdown, click_button


class AlertsPage(BasePage):

    def open(self):
        return self.visit(
            site_name="apac-reporting",
            page_name="alerts"
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

        click_button(
            uiform,
            "gridField_recordData_refreshButton",
            True
        )
        return uiform

    def clear_filters(self, uiform):
        if not uiform:
            return None

        click_button(
            uiform,
            "Clear Filters Option"
        )
        return uiform

    def filter_country(self, uiform, country):
        if not uiform:
            return None

        select_dropdown(
            uiform,
            "Countries",
            country
        )
        return uiform

    def export_report(self, uiform):
        if not uiform:
            return None

        click_button(
            uiform,
            "gridField_recordData_dataExportButton",
            True
        )
        return uiform
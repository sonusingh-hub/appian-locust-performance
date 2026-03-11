from core.base_page import BasePage
from core.ui_helpers import select_multi_dropdown, click_button


class ManageUserPage(BasePage):

    def open(self):
        return self.visit(
            site_name="apac-reporting",
            page_name="manage-user"
        )

    def search_record(self, uiform, value):
        if not uiform:
            return None

        new_uiform = uiform.fill_text_field(
            label="recordSearchBox",
            value=value,
            is_test_label=True
        )
        return new_uiform

    def click_search_box(self, uiform):
        if not uiform:
            return None

        new_uiform = uiform.click(
            label="recordSearchBox",
            is_test_label=True
        )
        return new_uiform

    def filter_user_group(self, uiform, values):
        if not uiform:
            return None

        return select_multi_dropdown(
            uiform,
            "userFilterDropdown_1",
            values
        )

    def export_report(self, uiform):
        if not uiform:
            return None

        return click_button(
            uiform,
            "gridField_recordData_dataExportButton",
            True
        )

    def clear_filters(self, uiform):
        if not uiform:
            return None

        return click_button(
            uiform,
            "Clear Filters Option"
        )
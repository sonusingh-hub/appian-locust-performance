from core.base_page import BasePage
from core.ui_helpers import click_button
from utils.waits import small_wait


class AdminConfigurationPage(BasePage):

    def open(self):
        return self.visit(
            site_name="apac-reporting",
            page_name="admin-configuration"
        )

    def open_industry_trends(self, uiform):
        if not uiform:
            return None

        # safest first attempt: plain click by visible label
        new_uiform = uiform.click(
            label="Industry Trends"
        )
        small_wait()
        return new_uiform

    def cancel(self, uiform):
        if not uiform:
            return None

        return click_button(
            uiform,
            "Cancel"
        )

    def refresh_after_update(self, uiform):
        if not uiform:
            return None

        return click_button(
            uiform,
            "updateRecordActionRefresh"
        )
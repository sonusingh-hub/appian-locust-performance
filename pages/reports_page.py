from core.base_page import BasePage
from core.ui_helpers import select_dropdown


class ReportsPage(BasePage):

    def open_fleet_schedule(self):
        return self.visit(
            site_name="apac-reporting",
            page_name="fleet-schedule"
        )

    def select_month(self, uiform, month):
        if not uiform:
            return None

        select_dropdown(
            uiform,
            "Month",
            month
        )
        return uiform
from core.base_page import BasePage
from core.ui_helpers import (
    click_button,
    click_clickable_by_text,
    has_component_label,
    has_component_text,
)


class AdminConfigurationPage(BasePage):
    UPDATE_RECORD_REFRESH_LABEL = "updateRecordActionRefresh"

    def open(self):
        return self.visit(
            site_name="apac-reporting",
            page_name="admin-configuration",
        )

    def open_industry_trends(self, uiform):
        if not uiform:
            return None

        if has_component_text(uiform, "Industry Trends"):
            updated = click_clickable_by_text(uiform, "Industry Trends", timeout=3)
            if updated:
                return updated

        return uiform

    def open_manage(self, uiform):
        if not uiform:
            return None

        if has_component_text(uiform, "Manage"):
            updated = click_clickable_by_text(uiform, "Manage", timeout=3)
            if updated:
                return updated

        return uiform

    def cancel_action_dialog(self, uiform):
        if not uiform:
            return None

        if has_component_label(uiform, "Cancel"):
            updated = click_button(
                uiform,
                "Cancel",
                timeout=3,
            )
            if updated:
                return updated

        if has_component_text(uiform, "Cancel"):
            updated = click_clickable_by_text(uiform, "Cancel", timeout=2)
            if updated:
                return updated

        return uiform

    def refresh_after_action(self, uiform):
        if not uiform:
            return None

        if has_component_label(uiform, self.UPDATE_RECORD_REFRESH_LABEL):
            updated = click_button(
                uiform,
                self.UPDATE_RECORD_REFRESH_LABEL,
                timeout=2,
            )
            if updated:
                return updated

        if has_component_label(
            uiform,
            self.UPDATE_RECORD_REFRESH_LABEL,
            is_test_label=True,
        ):
            updated = click_button(
                uiform,
                self.UPDATE_RECORD_REFRESH_LABEL,
                is_test_label=True,
                timeout=2,
            )
            if updated:
                return updated

        if has_component_text(uiform, "Refresh"):
            updated = click_clickable_by_text(uiform, "Refresh", timeout=2)
            if updated:
                return updated

        return uiform

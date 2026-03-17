from core.base_page import BasePage
from core.ui_helpers import (
    click_button,
    click_field,
    fill_text_field,
    has_component_label,
    has_component_text,
    has_component_icon,
    click_clickable_by_text,
    click_clickable_by_icon,
)
import logging


log = logging.getLogger(__name__)


class ManageUserPage(BasePage):
    SEARCH_BOX_TEST_LABEL = "recordSearchBox"
    USER_FILTER_TEST_LABEL = "userFilterDropdown_1"
    EXPORT_BUTTON_TEST_LABEL = "gridField_recordData_dataExportButton"
    REFRESH_BUTTON_TEST_LABEL = "gridField_recordData_refreshButton"
    UPDATE_RECORD_REFRESH_LABEL = "updateRecordActionRefresh"
    RELATED_ACTION_LABEL_VARIANTS = {
        "Edit Permissions": ["Edit Permissions"],
        "Delete User and User Permission": [
            "Delete User and User Permission",
            "Delete User and User Permissions",
            "Delete User & User Permission",
            "Delete User",
        ],
        "View History": ["View History", "History"],
    }
    RELATED_ACTION_ICON_BY_LABEL = {
        "Edit Permissions": "user-edit",
        "Delete User and User Permission": "user-times",
        "View History": "history",
    }

    def open(self):
        return self.visit(
            site_name="apac-reporting",
            page_name="manage-user",
        )

    def search_record(self, uiform, value):
        if not uiform:
            return None

        return fill_text_field(
            uiform,
            label=self.SEARCH_BOX_TEST_LABEL,
            value=value,
            is_test_label=True,
            timeout=3,
        )

    def click_search_box(self, uiform):
        if not uiform:
            return None

        return click_field(
            uiform,
            label=self.SEARCH_BOX_TEST_LABEL,
            is_test_label=True,
            timeout=3,
        )

    def clear_search(self, uiform):
        if not uiform:
            return None

        return self.search_record(uiform, "")

    def apply_user_groups(self, uiform, groups):
        if not uiform:
            return None

        return uiform.select_multi_dropdown_item(
            label=self.USER_FILTER_TEST_LABEL,
            choice_label=groups,
            is_test_label=True,
        )

    def export_grid(self, uiform):
        if not uiform:
            return None

        return click_button(
            uiform,
            self.EXPORT_BUTTON_TEST_LABEL,
            is_test_label=True,
            timeout=3,
        )

    def refresh_grid(self, uiform):
        if not uiform:
            return None

        return click_button(
            uiform,
            self.REFRESH_BUTTON_TEST_LABEL,
            is_test_label=True,
            timeout=3,
        )

    def open_related_action(self, uiform, action_label):
        if not uiform:
            return None

        candidates = self.RELATED_ACTION_LABEL_VARIANTS.get(action_label, [action_label])

        icon_name = self.RELATED_ACTION_ICON_BY_LABEL.get(action_label)
        if icon_name and has_component_icon(uiform, icon_name):
            updated = click_clickable_by_icon(uiform, icon_name, timeout=2)
            if updated:
                return updated

        for candidate in candidates:
            if not has_component_label(uiform, candidate):
                continue

            try:
                return uiform.click_related_action(label=candidate)
            except Exception:
                log.warning("Related action click failed for label '%s'.", candidate)

        for candidate in candidates:
            if not has_component_text(uiform, candidate):
                continue

            updated = click_clickable_by_text(uiform, candidate, timeout=2)
            if updated:
                return updated

        if has_component_text(uiform, action_label):
            updated = click_clickable_by_text(uiform, action_label, timeout=2)
            if updated:
                return updated

        log.warning("Related action not found; skipping '%s'.", action_label)
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

    def refresh_after_related_action(self, uiform):
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

        # This control is transient on Manage User; continue flow if absent.
        return uiform

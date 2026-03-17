import logging

from pages.home_page import HomePage
from core.ui_helpers import (
    click_record_list_action,
    click_start_process_link,
    click_linked_item_by_caption,
    click_clickable_by_text,
    click_field,
    click_button,
    select_dropdown,
    select_dropdown_test_label,
    fill_picker_field,
    click_clickable_by_icon,
)


log = logging.getLogger(__name__)


class VehicleSearchPage(HomePage):

    @staticmethod
    def _iter_components(node):
        if isinstance(node, dict):
            yield node
            for value in node.values():
                yield from VehicleSearchPage._iter_components(value)
        elif isinstance(node, list):
            for item in node:
                yield from VehicleSearchPage._iter_components(item)

    def _has_vehicle_search_popup(self, uiform):
        if not uiform or not hasattr(uiform, "_state"):
            return False

        markers = (
            "Search Vehicle",
            "Find vehicle details by entering the country and registration number.",
            "test-Registration",
            "Registration",
            "-- Select a Value --",
        )

        for component in self._iter_components(uiform._state):
            if not isinstance(component, dict):
                continue

            for key in (
                "label",
                "testLabel",
                "text",
                "caption",
                "#v",
                "placeholder",
                "accessibilityText",
                "ariaLabel",
            ):
                value = component.get(key)
                if not isinstance(value, str):
                    continue

                for marker in markers:
                    if marker in value:
                        return True

        return False

    def open_vehicle_search(self, uiform):
        if not uiform:
            return None

        # Try multiple open paths and only return when popup markers are visible.
        open_attempts = [
            lambda ui: click_start_process_link(ui, "Vehicle Search", timeout=3),
            lambda ui: click_start_process_link(ui, "Vehicle Search", is_test_label=True, timeout=3),
            lambda ui: click_linked_item_by_caption(ui, "Vehicle Search", timeout=3),
            lambda ui: click_clickable_by_text(ui, "Vehicle Search", timeout=3),
            lambda ui: click_field(ui, "Vehicle Search", timeout=3),
            lambda ui: click_field(ui, "Vehicle Search", is_test_label=True, timeout=3),
            lambda ui: click_record_list_action(ui, "Vehicle Search", timeout=3),
        ]

        for attempt in open_attempts:
            updated = attempt(uiform)
            if updated and self._has_vehicle_search_popup(updated):
                return updated

        # Some environments require opening an action menu first.
        menu_opened = click_button(uiform, "thirty_seconds", is_test_label=True, timeout=3)
        if menu_opened:
            updated = click_clickable_by_text(menu_opened, "Vehicle Search", timeout=3)
            if updated and self._has_vehicle_search_popup(updated):
                return updated

            updated = click_record_list_action(menu_opened, "Vehicle Search", timeout=3)
            if updated and self._has_vehicle_search_popup(updated):
                return updated

        log.warning("Vehicle Search popup did not open after all known strategies.")
        return None

    def select_country(self, uiform, country):
        if not uiform:
            return None

        if not self._has_vehicle_search_popup(uiform):
            log.warning("Vehicle Search popup is not open; cannot select country.")
            return None

        updated = select_dropdown(uiform, "Country", country, timeout=3)
        if updated:
            return updated

        updated = select_dropdown_test_label(uiform, "Country", country, timeout=3)
        if updated:
            return updated

        updated = select_dropdown_test_label(uiform, "test-Country", country, timeout=3)
        if updated:
            return updated

        opened = click_clickable_by_text(uiform, "-- Select a Value --", timeout=3)
        if opened:
            selected = click_clickable_by_text(opened, country, timeout=5)
            if selected:
                return selected

        opened = click_clickable_by_text(uiform, "Country", timeout=3)
        if opened:
            selected = click_clickable_by_text(opened, country, timeout=5)
            if selected:
                return selected

        return uiform

    def fill_registration(self, uiform, registration):
        if not uiform:
            return None

        if not self._has_vehicle_search_popup(uiform):
            log.warning("Vehicle Search popup is not open; cannot fill registration.")
            return None

        # Type the registration token progressively (e.g. N -> NE -> NET23F)
        # so picker suggestions can appear, then select the displayed value.
        token = registration
        if isinstance(registration, str) and " - " in registration:
            token = registration.split(" - ", 1)[0].strip()

        if not isinstance(token, str) or not token.strip():
            return uiform

        token = token.strip()

        start_len = 3 if len(token) >= 3 else 1
        for i in range(start_len, len(token) + 1):
            partial_value = token[:i]
            updated = fill_picker_field(
                uiform,
                label="test-Registration",
                value=partial_value,
                identifier="#v",
                format_test_label=False,
                timeout=2,
            )
            if updated:
                return updated

        log.warning(
            "Vehicle Search registration picker could not resolve suggestions for value '%s'.",
            registration,
        )
        return uiform

    def reset_vehicle_search_filters(self, uiform):
        if not uiform:
            return None

        return click_clickable_by_icon(uiform, "eraser", timeout=3)
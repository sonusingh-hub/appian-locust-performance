import logging
import random

from core.base_page import BasePage
from core.ui_helpers import (
    click_linked_item_by_caption,
    select_dropdown,
    select_multi_dropdown,
    click_button,
    click_clickable_by_text,
    click_clickable_by_icon,
    get_multi_dropdown_choices,
    fill_text_field,
)
from utils.waits import small_wait

log = logging.getLogger(__name__)


class ReportsNavigationPage(BasePage):
    """Base class for every Reports page.

    Owns:
    - Left-pane navigation methods (open_alerts, open_fleet_schedule, …)
    - The four global filters shared across all Reports pages
      (Country → Client Group → Client Name → Bill To)
    - apply_global_filters() / reset_global_filters() for journey-level use
    """

    # ── Global filter helpers ──────────────────────────────────────────────

    def _select_available_values(self, uiform, label, preferred_values=None, count=1):
        """Pick values for a multi-dropdown from the live choices Appian exposes.

        Cascading dropdowns (e.g. Client Group depends on Country) mean the
        available choices change after each selection.  This method always reads
        the *current* live choices, tries to honour preferred_values
        (case-insensitive), and falls back to a random valid pick so the
        request never fails due to a stale static list.
        """
        if not uiform:
            return None

        available_choices = get_multi_dropdown_choices(uiform, label)
        if not available_choices:
            log.warning("No choices available for '%s'; skipping selection.", label)
            return uiform

        selected_values = []
        if preferred_values:
            normalised = {c.casefold(): c for c in available_choices}
            for preferred in preferred_values:
                resolved = normalised.get(str(preferred).casefold())
                if resolved and resolved not in selected_values:
                    selected_values.append(resolved)
                if len(selected_values) >= count:
                    break

        if not selected_values:
            selected_values = random.sample(
                available_choices, k=min(count, len(available_choices))
            )

        return select_multi_dropdown(uiform, label, selected_values)

    def select_country(self, uiform, countries=None):
        """Select Country from currently available choices."""
        preferred = countries if isinstance(countries, list) else ([countries] if countries else None)
        return self._select_available_values(uiform, "Country", preferred_values=preferred, count=1)

    def select_client_group(self, uiform, client_groups=None):
        """Select Client Group from currently available choices (depends on Country)."""
        preferred = client_groups if isinstance(client_groups, list) else ([client_groups] if client_groups else None)
        return self._select_available_values(uiform, "Client Group", preferred_values=preferred, count=1)

    def select_client_name(self, uiform, client_names=None):
        """Select Client Name from currently available choices (depends on Client Group)."""
        preferred = client_names if isinstance(client_names, list) else ([client_names] if client_names else None)
        return self._select_available_values(uiform, "Client Name", preferred_values=preferred, count=1)

    def select_bill_to(self, uiform, bill_to_values=None):
        """Select Bill To from currently available choices."""
        preferred = bill_to_values if isinstance(bill_to_values, list) else ([bill_to_values] if bill_to_values else None)
        return self._select_available_values(uiform, "Bill To", preferred_values=preferred, count=1)

    def apply_global_filters(
        self,
        uiform,
        filter_state,
        *,
        countries=None,
        client_groups=None,
        client_names=None,
        bill_to_values=None,
    ):
        """Apply all four global filters in cascade order and record results in filter_state.

        Country is selected first; Appian then updates the available Client Group
        choices.  Client Group is selected next, which updates Client Name choices,
        and so on.  Each step passes the freshly updated uiform forward so the
        cascading choices are always read from the latest UI state.

        Partial failures (e.g. Bill To not available) are logged and skipped rather
        than aborting the whole sequence so the test still exercises the earlier
        filter selections.
        """
        if not uiform:
            return None

        current = self.select_country(uiform, countries)
        if current:
            filter_state.country = countries or []
            uiform = current

        current = self.select_client_group(uiform, client_groups)
        if current:
            filter_state.client_group = client_groups or []
            uiform = current

        current = self.select_client_name(uiform, client_names)
        if current:
            filter_state.client_name = client_names or []
            uiform = current

        current = self.select_bill_to(uiform, bill_to_values)
        if current:
            filter_state.bill_to = bill_to_values or []
            uiform = current

        filter_state.is_applied = True
        return uiform

    def reset_global_filters(self, uiform, filter_state=None):
        """Reset all global report filters and clear filter_state.

        Tries (in order):
          1. Eraser icon button  (new UI)
          2. 'Reset Filters' clickable text
          3. 'Clear Filters Option' button  (legacy fallback)

        When filter_state is provided it is cleared on success so the next task
        knows it must re-apply filters from scratch.
        """
        if not uiform:
            return None

        updated = click_clickable_by_icon(uiform, "eraser", timeout=3)
        if not updated:
            updated = click_clickable_by_text(uiform, "Reset Filters", timeout=3)
        if not updated:
            updated = click_button(uiform, "Clear Filters Option", timeout=3)

        if updated is not None and filter_state is not None:
            filter_state.clear()

        return updated or uiform

    def open_vehicle_search(self, uiform):
        if not uiform:
            return None

        # Vehicle Search is now available from all reports pages.
        return click_clickable_by_text(uiform, "Vehicle Search")

    def select_vehicle_search_country(self, uiform, country):
        if not uiform:
            return None

        # Vehicle Search country can render as either single or multi dropdown.
        updated = select_dropdown(uiform, "Country", country, timeout=3)
        if updated:
            return updated

        updated = select_multi_dropdown(uiform, "Country", [country], timeout=3)
        if updated:
            return updated

        log.warning(
            "Vehicle Search country control not found; skipping country selection for '%s'.",
            country,
        )
        return uiform

    def fill_registration(self, uiform, registration):
        if not uiform:
            return None

        label_candidates = [
            ("Registration", False),
            ("Registration", True),
            ("Registration and/or Chassis", False),
            ("Registration and/or Chassis", True),
            ("recordSearchBox", True),
            ("Vehicle Search-recordSearchBox", True),
        ]

        for label, is_test_label in label_candidates:
            updated = fill_text_field(
                uiform,
                label=label,
                value=registration,
                is_test_label=is_test_label,
                timeout=3,
            )
            if updated:
                return updated

        return None

    # ── Left-pane navigation ──────────────────────────────────────────────

    def _reset_export_card_gate(self):
        self._export_card_selected = False

    def _mark_export_card_selected(self):
        self._export_card_selected = True

    def _is_export_card_selected(self):
        return bool(getattr(self, "_export_card_selected", False))

    def open_reports(self):
        self._reset_export_card_gate()
        uiform = self.visit(
            site_name="apac-reporting",
            page_name="reports"
        )
        if not uiform:
            return None

        small_wait()
        return uiform

    def _open_left_pane_item(self, uiform, label):
        if not uiform:
            return None

        # New reports navigation icons expose aria-label text; try text/aria matching
        # click first, then fall back to legacy LinkedItem behavior.
        updated = click_clickable_by_text(uiform, label, timeout=3)
        if not updated:
            updated = click_linked_item_by_caption(uiform, label, timeout=3)

        small_wait()
        return updated

    def open_alerts(self, uiform):
        return self._open_left_pane_item(uiform, "Alerts")

    def open_fleet_schedule(self, uiform):
        return self._open_left_pane_item(uiform, "Fleet Schedule")

    def open_vehicle_on_order(self, uiform):
        return self._open_left_pane_item(uiform, "Vehicles On Order")

    def open_imminent_expiry(self, uiform):
        return self._open_left_pane_item(uiform, "Imminent Contract Expiry")

    def open_sustainability(self, uiform):
        return self._open_left_pane_item(uiform, "Sustainability")

    def open_vehicle_utilisation(self, uiform):
        return self._open_left_pane_item(uiform, "Vehicle Utilisation")

    def open_service_overdue(self, uiform):
        return self._open_left_pane_item(uiform, "Service Overdue")

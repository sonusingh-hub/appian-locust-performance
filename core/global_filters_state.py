from dataclasses import dataclass, field


@dataclass
class GlobalFiltersState:
    """Per-VUser mirror of the four global report filters.

    Appian persists filter selections server-side across every Reports page
    within the same session.  When a VUser applies Country on the Home page,
    the Alerts page (and every other report page) already shows that country
    selected — no re-application is needed.

    This dataclass lets journeys:
    - Track which values were selected so they can be re-used when needed.
    - Skip re-applying filters they have already set (is_applied flag).
    - Know when a reset has occurred so the next task can re-apply cleanly.

    Usage in a journey:
        # Apply once at the start of a session block
        if not self.filter_state.is_applied:
            uiform = page.apply_global_filters(
                uiform, self.filter_state,
                countries=DataEngine.home_country_list(),
            )

        # Reset from any page — clears state so next task re-applies
        uiform = page.reset_global_filters(uiform, self.filter_state)
    """

    country: list = field(default_factory=list)
    client_group: list = field(default_factory=list)
    client_name: list = field(default_factory=list)
    bill_to: list = field(default_factory=list)
    is_applied: bool = False

    def clear(self):
        """Clear all stored filter values and mark as not applied."""
        self.country.clear()
        self.client_group.clear()
        self.client_name.clear()
        self.bill_to.clear()
        self.is_applied = False

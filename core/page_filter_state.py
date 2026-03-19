from dataclasses import dataclass, field


@dataclass
class PageFilterState:
    """Per-page filter tracking for optimized reapplication.

    Each report page (Fleet Schedule, Vehicle On Order, etc.) maintains filters
    that may persist across multiple user actions and tasks for the same virtual
    user session.

    By tracking which filter values were last applied, journeys can skip
    redundant filter operations when values haven't changed, reducing UI overhead
    and script load while maintaining realistic filter behavior.

    Usage in a page:
        In page's select_product method:
            if self.page_filter_state.is_filter_set("product", products):
                return uiform  # Skip, already set
            uiform = select_multi_dropdown(...)
            self.page_filter_state.set_filter("product", products)
            return uiform

    Usage on reset:
        When filters are explicitly cleared in the UI:
            self.reset_page_filters()

    The state is stored at taskset/user scope so recreating page objects between
    Locust tasks does not discard the cached selections.
    """

    filters: dict = field(default_factory=dict)

    def set_filter(self, filter_name, value):
        """Record that a filter has been applied with given value."""
        if value is None:
            return
        self.filters[filter_name] = value

    def is_filter_set(self, filter_name, value):
        """Check if filter with this exact value is already set."""
        if value is None:
            return False

        if filter_name not in self.filters:
            return False

        stored = self.filters[filter_name]

        # Handle list/tuple comparisons (for multi-select)
        if isinstance(stored, (list, tuple)) and isinstance(value, (list, tuple)):
            return sorted(stored) == sorted(value)

        return stored == value

    def reset(self):
        """Clear all tracked filter values."""
        self.filters.clear()

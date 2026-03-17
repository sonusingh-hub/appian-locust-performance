from pages.reports_navigation_page import ReportsNavigationPage


class HomePage(ReportsNavigationPage):
    """Page object for the Reports landing (Home) page.

    The Home page is what `visit_site("apac-reporting", "reports")` loads.
    All four global filters (Country, Client Group, Client Name, Bill To) and
    reset_global_filters() are inherited from ReportsNavigationPage so they
    are available on every Reports page without duplication.
    """

    def open(self):
        return self.open_reports()

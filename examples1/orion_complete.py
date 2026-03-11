from appian_locust import AppianTaskSet
from locust import HttpUser, task, between
import time
import random


class OrionPerfTasks(AppianTaskSet):
    """Tasks modelling Login + Report View / Search / Export with realistic waits."""

    def cascade_wait(self, min_s=0.5, max_s=2.0):
        time.sleep(random.uniform(min_s, max_s))

    def on_start(self):
        # ensure user session / landing page is loaded (framework will use HttpUser.auth)
        try:
            self.appian.visitor.visit_site(site_name="apac-reporting", page_name="home")
        except Exception:
            pass

    @task(70)
    def view_reports(self):
        """70% weight: navigate to reporting pages and view reports (landing + many views)."""
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting", page_name="fleet-schedule")
        if not uiform:
            return
        # sample view interactions
        uiform.select_dropdown_item(label="Month", choice_label="Jan 2026")
        self.cascade_wait()
        uiform.select_multi_dropdown_item(label="Product", choice_label=["Finance"])
        self.cascade_wait()
        uiform.select_multi_dropdown_item(label="Vehicle Type", choice_label=["Light Commercial"])
        self.cascade_wait()
        # jump to other report pages to simulate browsing
        self.appian.visitor.visit_site(site_name="apac-reporting", page_name="vehicle-on-order")
        self.cascade_wait()
        self.appian.visitor.visit_site(site_name="apac-reporting", page_name="vehicle-utilisation")
        self.cascade_wait()

    @task(50)
    def search_and_filter(self):
        """50% weight: perform search & filter operations across reports."""
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting", page_name="alerts")
        if uiform:
            uiform.fill_text_field(label="recordSearchBox", value="Colgate Palmolive Pty Ltd", is_test_label=True)
            self.cascade_wait()
            uiform.click(label="recordSearchBox", is_test_label=True)
            self.cascade_wait()
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting", page_name="imminent-expiry")
        if uiform:
            uiform.select_dropdown_item(label="Month", choice_label="Jan 2026")
            self.cascade_wait()
            uiform.select_multi_dropdown_item(label="Product", choice_label=["Operating"])
            self.cascade_wait()

    @task(20)
    def export_report(self):
        """20% weight: trigger export/report download actions."""
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting", page_name="alerts")
        if uiform:
            # attempt export action (non-blocking in load test)
            try:
                uiform.click(label="gridField_recordData_dataExportButton", is_test_label=True)
            except Exception:
                pass
            self.cascade_wait()
        # also simulate export from fleet-schedule
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting", page_name="fleet-schedule")
        if uiform:
            try:
                uiform.click(label="gridField_recordData_dataExportButton", is_test_label=True)
            except Exception:
                pass
            self.cascade_wait()


class UserActor(HttpUser):
    tasks = [OrionPerfTasks]
    host = "https://orion-preprodanz.orix.com.au"    # base URL (no /suite/portal/login.jsp)
    auth = ["apac_nestle", "ORIX@2025"]             # replace with secure storage in real runs
    wait_time = between(1, 3)
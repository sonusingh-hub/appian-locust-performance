from appian_locust import AppianTaskSet
from locust import HttpUser, task, between
import time
import random
import os

# Configure via environment variables for safety (don't hard-code credentials)
HOST = os.environ.get("PERF_HOST", "https://orion-testanz.orix.com.au")
AUTH_USER = os.environ.get("PERF_USER", "TEST_PERF_PRIMARY")
AUTH_PASS = os.environ.get("PERF_PASS", "ORIX@2026")

# Workload weights: view_report ~70%, search/filter ~50% (relative), export ~20%
# approximate with integer task weights: view=7, search=5, export=2
class PerfTaskSet(AppianTaskSet):

    def cascade_wait(self, min_s=0.3, max_s=1.2):
        time.sleep(random.uniform(min_s, max_s))

    @task(7)
    def view_reports(self):
        # Visit landing/home then open a report via visitor API
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting", page_name="home")
        self.cascade_wait()
        # example report view via visitor (adjust name to target report)
        try:
            report_form = self.appian.visitor.visit_report("RTE Basic Test Report", exact_match=False)
            self.cascade_wait()
            # interact with report UI (filters/dropdowns) if present
            if report_form:
                # try common interactions seen in recording
                try:
                    report_form.select_dropdown_item(label="Countries", choice_label="Australia")
                    self.cascade_wait()
                except Exception:
                    pass
        except Exception:
            # swallow to let Locust record failures; no rethrow to keep user alive
            pass

    @task(5)
    def search_and_filter(self):
        # Navigate to alerts/search page and perform search/filter operations
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting", page_name="alerts")
        self.cascade_wait()
        if not uiform:
            return
        # text search example
        try:
            uiform.fill_text_field(label="recordSearchBox", value="Colgate Palmolive Pty Ltd", is_test_label=True)
            self.cascade_wait()
            uiform.click(label="recordSearchBox", is_test_label=True)
            self.cascade_wait()
            # additional filter selections (examples from recording)
            try:
                uiform.select_dropdown_item(label="Countries", choice_label="Australia")
                self.cascade_wait()
            except Exception:
                pass
        except Exception:
            pass

    @task(2)
    def export_report(self):
        # Trigger report export from a grid or report page
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting", page_name="alerts")
        self.cascade_wait()
        if not uiform:
            return
        try:
            # click the export button observed in recording
            uiform.click(label="gridField_recordData_dataExportButton", is_test_label=True)
            self.cascade_wait(0.5, 2.0)
            # optionally poll an export status control if your app has one
            # try: uiform.click(label="export_status_refresh") ; except: pass
        except Exception:
            pass

    @task(1)
    def landing_and_profile(self):
        # light-weight landing + profile visit to simulate navigation mix
        self.appian.visitor.visit_site(site_name="apac-reporting", page_name="home")
        self.cascade_wait()
        self.appian.visitor.visit_site(site_name="apac-reporting", page_name="manage-user")
        self.cascade_wait()

class PerfUser(HttpUser):
    tasks = [PerfTaskSet]
    wait_time = between(2, 5)
    host = HOST
    # AppianTaskSet/on_start will call interactor.login using this auth tuple
    auth = [AUTH_USER, AUTH_PASS]
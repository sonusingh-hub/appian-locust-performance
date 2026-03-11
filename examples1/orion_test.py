# ...existing code...
from appian_locust import AppianTaskSet
from locust import HttpUser, task, between
import time
import random


class GeneratedTaskSet(AppianTaskSet):

    def cascade_wait(self, min_s=0.3, max_s=1.2):
        """Small randomized wait to mimic UI cascades between selections."""
        time.sleep(random.uniform(min_s, max_s))

    @task
    def recorded_interactions(self):
        # start at a known page so uiform is valid
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting", page_name="home")

        if uiform:
            uiform.select_dropdown_item(label="Countries", choice_label="Australia")
            self.cascade_wait()
            uiform.select_dropdown_item(label="Countries", choice_label="New Zealand")
            self.cascade_wait()
            # uiform.click_record_list_action(label="Search Vehicle")
            # self.cascade_wait()
            # uiform.select_dropdown_item(label="Country", choice_label="Australia")
            # self.cascade_wait()
            # uiform.fill_picker_field(label="test-Registration",
            #                          value="NET23F - JTNKY3BX401029374",
            #                          format_test_label=False,
            #                          identifier="#v")
            # self.cascade_wait()

        # alerts
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting", page_name="alerts")
        if uiform:
            uiform.fill_text_field(label="recordSearchBox",
                                   value="Colgate Palmolive Pty Ltd",
                                   is_test_label=True)
            self.cascade_wait()
            uiform.click(label="recordSearchBox", is_test_label=True)
            self.cascade_wait()
            uiform.click(label="gridField_recordData_dataExportButton", is_test_label=True)
            self.cascade_wait()
            uiform.select_dropdown_item(label="Countries", choice_label="Australia")
            self.cascade_wait()

        # fleet-schedule
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting", page_name="fleet-schedule")
        if uiform:
            uiform.select_dropdown_item(label="Month", choice_label="Jan 2026")
            self.cascade_wait()
            uiform.select_multi_dropdown_item(label="Product", choice_label=["Finance"])
            self.cascade_wait()
            uiform.select_multi_dropdown_item(label="Product", choice_label=["Finance", "Operating"])
            self.cascade_wait()
            uiform.select_multi_dropdown_item(label="Vehicle Type", choice_label=["Light Commercial"])
            self.cascade_wait()
            uiform.select_multi_dropdown_item(label="Vehicle Type", choice_label=["Light Commercial", "Passenger"])
            self.cascade_wait()
            uiform.select_dropdown_item(label="Imminent Expiry", choice_label="Next 6 Months")
            self.cascade_wait()
            uiform.select_multi_dropdown_item(label="Power Train", choice_label=["Battery Electric Vehicle"])
            self.cascade_wait()
            uiform.select_multi_dropdown_item(label="Power Train", choice_label=["Battery Electric Vehicle", "Hybrid Electric Vehicle"])
            self.cascade_wait()

        # vehicle-on-order
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting", page_name="vehicle-on-order")
        if uiform:
            uiform.select_multi_dropdown_item(label="Product", choice_label=["Finance Lease"])
            self.cascade_wait()
            uiform.select_multi_dropdown_item(label="Product", choice_label=["Finance Lease", "Operating Lease"])
            self.cascade_wait()
            uiform.select_multi_dropdown_item(label="Vehicle Type", choice_label=["Light Commercial"])
            self.cascade_wait()
            uiform.select_multi_dropdown_item(label="Vehicle Type", choice_label=["Light Commercial", "Passenger"])
            self.cascade_wait()
            uiform.select_multi_dropdown_item(label="Power Train", choice_label=["Hybrid Electric Vehicle"])
            self.cascade_wait()
            uiform.select_dropdown_item(label="Expected Delivery", choice_label="6 Months")
            self.cascade_wait()

        # imminent-expiry
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting", page_name="imminent-expiry")
        if uiform:
            uiform.select_dropdown_item(label="Month", choice_label="Jan 2026")
            self.cascade_wait()
            uiform.select_multi_dropdown_item(label="Product", choice_label=["Operating"])
            self.cascade_wait()
            uiform.select_multi_dropdown_item(label="Vehicle Type", choice_label=["Passenger"])
            self.cascade_wait()
            uiform.select_dropdown_item(label="Imminent Expiry", choice_label="Next 6 Months")
            self.cascade_wait()
            uiform.select_multi_dropdown_item(label="Power Train", choice_label=["Hybrid Electric Vehicle"])
            self.cascade_wait()

        # sustainability
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting", page_name="sustainability")
        if uiform:
            uiform.select_multi_dropdown_item(label="Product", choice_label=["Operating"])
            self.cascade_wait()
            uiform.select_multi_dropdown_item(label="Vehicle Type", choice_label=["Passenger"])
            self.cascade_wait()
            uiform.select_multi_dropdown_item(label="Power Train", choice_label=["Hybrid Electric Vehicle"])
            self.cascade_wait()

        # vehicle-utilisation
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting", page_name="vehicle-utilisation")
        if uiform:
            uiform.select_dropdown_item(label="Month", choice_label="Jan 2026")
            self.cascade_wait()
            uiform.select_multi_dropdown_item(label="Product", choice_label=["Novated Finance"])
            self.cascade_wait()
            uiform.select_multi_dropdown_item(label="Product", choice_label=["Novated Finance", "Operating"])
            self.cascade_wait()
            uiform.select_multi_dropdown_item(label="Vehicle Type", choice_label=["Trailer"])
            self.cascade_wait()
            uiform.select_multi_dropdown_item(label="Vehicle Type", choice_label=["Trailer", "Passenger"])
            self.cascade_wait()
            uiform.select_dropdown_item(label="Imminent Expiry", choice_label="Next 12 Months")
            self.cascade_wait()
            uiform.select_multi_dropdown_item(label="Power Train", choice_label=["Battery Electric Vehicle"])
            self.cascade_wait()
            uiform.select_multi_dropdown_item(label="Power Train", choice_label=["Battery Electric Vehicle", "Hybrid Electric Vehicle"])
            self.cascade_wait()

        # service-overdue
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting", page_name="service-overdue")
        if uiform:
            uiform.select_dropdown_item(label="Month", choice_label="Jan 2026")
            self.cascade_wait()
            uiform.select_multi_dropdown_item(label="Product", choice_label=["Finance"])
            self.cascade_wait()
            uiform.select_dropdown_item(label="Overdue by", choice_label="KMs")
            self.cascade_wait()
            uiform.select_multi_dropdown_item(label="Vehicle Type", choice_label=["Passenger"])
            self.cascade_wait()
            uiform.select_multi_dropdown_item(label="Power Train", choice_label=["Hybrid Electric Vehicle"])
            self.cascade_wait()
            uiform.select_dropdown_item(label="Maintenance Included", choice_label="Yes")
            self.cascade_wait()

        # update-profile (selection only)
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting", page_name="update-profile")
        if uiform:
            uiform.select_dropdown_item(label="Language", choice_label="English(UK) [en_GB]")
            self.cascade_wait()

        # finish on home
        self.appian.visitor.visit_site(site_name="apac-reporting", page_name="process-hq")
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting", page_name="home")
        if uiform:
            try:
                uiform.click(label="async-variable-refresh")
            except Exception:
                pass

class UserActor(HttpUser):
    tasks = [GeneratedTaskSet]
    host = "https://orion-testanz.orix.com.au"
    auth = ["TEST_PERF_PRIMARY", "ORIX@2026"]
    wait_time = between(2, 5)

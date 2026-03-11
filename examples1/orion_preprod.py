from appian_locust import AppianTaskSet
from locust import HttpUser, task, between


class OrionTaskSet(AppianTaskSet):

    @task
    def recorded_interactions(self):
        # start from a known page so uiform is valid
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting", page_name="home")

        # Alerts page
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting", page_name="alerts")
        if uiform:
            uiform.select_dropdown_item(label="Countries", choice_label="Australia")

        # Fleet schedule
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting", page_name="fleet-schedule")
        if uiform:
            uiform.select_dropdown_item(label="Month", choice_label="Jan 2026")
            uiform.select_multi_dropdown_item(label="Country", choice_label=["Australia"])
            uiform.select_multi_dropdown_item(label="Country", choice_label=["Australia", "New Zealand"])
            uiform.select_multi_dropdown_item(label="Account Name", choice_label=["Nestle Australia Ltd (CPW)"])
            uiform.select_multi_dropdown_item(label="Product", choice_label=["Finance"])
            uiform.select_multi_dropdown_item(label="Vehicle Type", choice_label=["Light Commercial"])

        # Vehicle on order
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting", page_name="vehicle-on-order")
        if uiform:
            uiform.select_multi_dropdown_item(label="Country", choice_label=["Australia"])
            uiform.select_multi_dropdown_item(label="Country", choice_label=["Australia", "New Zealand"])
            uiform.select_multi_dropdown_item(label="Account Name", choice_label=["Nestle Australia Ltd"])
            uiform.select_multi_dropdown_item(label="Account Name", choice_label=["Nestle Australia Ltd", "Nestle Australia Ltd (CPW)"])
            uiform.select_multi_dropdown_item(label="Account Name", choice_label=["Nestle Australia Ltd (CPW)"])
            # clear selection
            uiform.select_multi_dropdown_item(label="Account Name", choice_label=[])

        # Imminent expiry
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting", page_name="imminent-expiry")
        if uiform:
            uiform.select_multi_dropdown_item(label="Country", choice_label=["Australia"])
            uiform.select_multi_dropdown_item(label="Country", choice_label=["Australia", "New Zealand"])

        # Sustainability
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting", page_name="sustainability")
        if uiform:
            uiform.select_multi_dropdown_item(label="Country", choice_label=["Australia"])
            uiform.select_multi_dropdown_item(label="Country", choice_label=["Australia", "New Zealand"])

        # Vehicle utilisation
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting", page_name="vehicle-utilisation")
        if uiform:
            uiform.select_multi_dropdown_item(label="Country", choice_label=["Australia"])
            uiform.select_multi_dropdown_item(label="Country", choice_label=["Australia", "New Zealand"])

        # Service overdue
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting", page_name="service-overdue")
        if uiform:
            uiform.select_multi_dropdown_item(label="Country", choice_label=["Australia"])
            uiform.select_multi_dropdown_item(label="Country", choice_label=["Australia", "New Zealand"])

        # Profile / management pages and return home
        self.appian.visitor.visit_site(site_name="apac-reporting", page_name="update-profile")
        self.appian.visitor.visit_site(site_name="apac-reporting", page_name="manage-user")
        self.appian.visitor.visit_site(site_name="apac-reporting", page_name="home")


class UserActor(HttpUser):
    tasks = [OrionTaskSet]
    host = "https://orion-preprodanz.orix.com.au"
    auth = ["apac_nestle", "ORIX@2025"]
    wait_time = between(2, 5)
# filepath: e:\appian-locust-main\examples\orion_preprod_full.py
from appian_locust import AppianTaskSet
from locust import HttpUser, task, between


class OrionTaskSet(AppianTaskSet):

    @task
    def recorded_interactions(self):
        # start from a known page so uiform is valid
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting", page_name="home")

        # Alerts page
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting", page_name="alerts")
        if uiform:
            uiform.select_dropdown_item(label="Countries", choice_label="Australia")

        # Fleet schedule
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting", page_name="fleet-schedule")
        if uiform:
            uiform.select_dropdown_item(label="Month", choice_label="Jan 2026")
            uiform.select_multi_dropdown_item(label="Country", choice_label=["Australia"])
            uiform.select_multi_dropdown_item(label="Country", choice_label=["Australia", "New Zealand"])
            uiform.select_multi_dropdown_item(label="Account Name", choice_label=["Nestle Australia Ltd (CPW)"])
            uiform.select_multi_dropdown_item(label="Product", choice_label=["Finance"])
            uiform.select_multi_dropdown_item(label="Vehicle Type", choice_label=["Light Commercial"])

        # Vehicle on order
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting", page_name="vehicle-on-order")
        if uiform:
            uiform.select_multi_dropdown_item(label="Country", choice_label=["Australia"])
            uiform.select_multi_dropdown_item(label="Country", choice_label=["Australia", "New Zealand"])
            uiform.select_multi_dropdown_item(label="Account Name", choice_label=["Nestle Australia Ltd"])
            uiform.select_multi_dropdown_item(label="Account Name", choice_label=["Nestle Australia Ltd", "Nestle Australia Ltd (CPW)"])
            uiform.select_multi_dropdown_item(label="Account Name", choice_label=["Nestle Australia Ltd (CPW)"])
            # clear selection
            uiform.select_multi_dropdown_item(label="Account Name", choice_label=[])

        # Imminent expiry
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting", page_name="imminent-expiry")
        if uiform:
            uiform.select_multi_dropdown_item(label="Country", choice_label=["Australia"])
            uiform.select_multi_dropdown_item(label="Country", choice_label=["Australia", "New Zealand"])

        # Sustainability
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting", page_name="sustainability")
        if uiform:
            uiform.select_multi_dropdown_item(label="Country", choice_label=["Australia"])
            uiform.select_multi_dropdown_item(label="Country", choice_label=["Australia", "New Zealand"])

        # Vehicle utilisation
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting", page_name="vehicle-utilisation")
        if uiform:
            uiform.select_multi_dropdown_item(label="Country", choice_label=["Australia"])
            uiform.select_multi_dropdown_item(label="Country", choice_label=["Australia", "New Zealand"])

        # Service overdue
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting", page_name="service-overdue")
        if uiform:
            uiform.select_multi_dropdown_item(label="Country", choice_label=["Australia"])
            uiform.select_multi_dropdown_item(label="Country", choice_label=["Australia", "New Zealand"])

        # Profile / management pages and return home
        self.appian.visitor.visit_site(site_name="apac-reporting", page_name="update-profile")
        self.appian.visitor.visit_site(site_name="apac-reporting", page_name="manage-user")
        self.appian.visitor.visit_site(site_name="apac-reporting", page_name="home")


class UserActor(HttpUser):
    tasks = [OrionTaskSet]
    host = "https://orion-preprodanz.orix.com.au"
    auth = ["apac_nestle", "ORIX@2025"]
    wait_time = between(2, 5)
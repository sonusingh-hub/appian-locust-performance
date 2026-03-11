from appian_locust import AppianTaskSet
from locust import HttpUser, task, between


class GeneratedTaskSet(AppianTaskSet):

    @task
    def recorded_interactions(self):
        # start on a known page so we get a valid uiform object
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting", page_name="home")

        # initial country dropdowns
        # if uiform:
        #     uiform.select_dropdown_item(value="-- Select Country --", choice_label="Australia")
        #     uiform.select_dropdown_item(value="-- Select Country --", choice_label="New Zealand")
        #     uiform.select_dropdown_item(value="-- Select Country --", choice_label="Thailand")

        # alerts page
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting", page_name="alerts")
        if uiform:
            uiform.fill_text_field(label="recordSearchBox",
                                   value="Nestle Australia Ltd (Operations)",
                                   is_test_label=True)
            uiform.click(label="recordSearchBox", is_test_label=True)
            uiform.fill_text_field(label="recordSearchBox", value="", is_test_label=True)
            uiform.click(label="gridField_recordData_dataExportButton",
                         is_test_label=True)

        # fleet schedule
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting", page_name="fleet-schedule")
        if uiform:
            uiform.select_multi_dropdown_item(label="Country", choice_label=["Australia"])
            uiform.select_multi_dropdown_item(label="Country",
                                              choice_label=["Australia", "New Zealand"])
            uiform.select_multi_dropdown_item(label="Account Name",
                                              choice_label=["Nestle Australia Ltd (CPW)"])
            uiform.select_multi_dropdown_item(label="Account Name",
                                              choice_label=["Nestle Australia Ltd (CPW)",
                                                            "Nestle Australia Ltd (Healthcare Nutrition)"])
            uiform.select_multi_dropdown_item(label="Product", choice_label=["Operating"])
            uiform.select_multi_dropdown_item(label="Product",
                                              choice_label=["Operating", "Finance"])
            uiform.select_multi_dropdown_item(label="Vehicle Type", choice_label=["Passenger"])
            uiform.select_multi_dropdown_item(label="Vehicle Type",
                                              choice_label=["Passenger", "Light Commercial"])
            uiform.select_dropdown_item(label="Imminent Expiry",
                                        choice_label="Next 12 Months")
            uiform.select_multi_dropdown_item(label="Power Train",
                                              choice_label=["Hybrid Electric Vehicle"])

        # vehicle‑on‑order
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting",
                                                page_name="vehicle-on-order")
        if uiform:
            uiform.select_multi_dropdown_item(label="Country", choice_label=["Australia"])
            uiform.select_multi_dropdown_item(label="Country",
                                              choice_label=["Australia", "New Zealand"])
            uiform.select_multi_dropdown_item(label="Account Name",
                                              choice_label=["Nestle Australia Ltd"])
            uiform.select_multi_dropdown_item(label="Account Name",
                                              choice_label=["Nestle Australia Ltd", "Nestle Australia Ltd (CPW)"])
            uiform.select_multi_dropdown_item(label="Product", choice_label=["Finance"])
            uiform.select_multi_dropdown_item(label="Product",
                                              choice_label=["Finance", "Operating"])
            uiform.select_multi_dropdown_item(label="Vehicle Type",
                                              choice_label=["Light Commercial"])
            uiform.select_multi_dropdown_item(label="Vehicle Type",
                                              choice_label=["Light Commercial", "Passenger"])
            uiform.select_multi_dropdown_item(label="Power Train",
                                              choice_label=["Hybrid Electric Vehicle"])
            uiform.select_multi_dropdown_item(label="Power Train",
                                              choice_label=["Hybrid Electric Vehicle",
                                                            "Internal Combustion Engine"])
            uiform.select_dropdown_item(label="Expected Delivery",
                                        choice_label="12 Months")
            uiform.select_dropdown_item(label="Year", choice_label="2024")

        # imminent‑expiry
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting",
                                                page_name="imminent-expiry")
        if uiform:
            uiform.select_multi_dropdown_item(label="Country", choice_label=["Australia"])
            uiform.select_multi_dropdown_item(label="Country",
                                              choice_label=["Australia", "New Zealand"])
            uiform.select_multi_dropdown_item(label="Account Name",
                                              choice_label=["Nestle Australia Ltd (Infant Nutrition)"])
            uiform.select_multi_dropdown_item(label="Account Name",
                                              choice_label=["Nestle Australia Ltd (Infant Nutrition)",
                                                            "Nestle Australia Ltd (Operations)"])
            uiform.select_multi_dropdown_item(label="Account Name",
                                              choice_label=["Nestle Australia Ltd (Infant Nutrition)",
                                                            "Nestle Australia Ltd (Operations)",
                                                            "Nestle Australia Ltd (CPW)"])
            uiform.select_multi_dropdown_item(label="Product", choice_label=["Finance"])
            uiform.select_multi_dropdown_item(label="Product",
                                              choice_label=["Finance", "Operating"])
            uiform.select_multi_dropdown_item(label="Vehicle Type",
                                              choice_label=["Light Commercial"])
            uiform.select_multi_dropdown_item(label="Vehicle Type",
                                              choice_label=["Light Commercial", "Passenger"])
            uiform.select_dropdown_item(label="Imminent Expiry",
                                        choice_label="Next 6 Months")
            uiform.select_multi_dropdown_item(label="Power Train",
                                              choice_label=["Hybrid Electric Vehicle"])

        # sustainability
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting",
                                                page_name="sustainability")
        if uiform:
            uiform.select_multi_dropdown_item(label="Country", choice_label=["Australia"])
            uiform.select_multi_dropdown_item(label="Country",
                                              choice_label=["Australia", "New Zealand"])
            uiform.select_multi_dropdown_item(label="Account Name",
                                              choice_label=["Nestle Australia Ltd (CPW)"])
            uiform.select_multi_dropdown_item(label="Account Name",
                                              choice_label=["Nestle Australia Ltd (CPW)",
                                                            "Nestle Australia Ltd (Healthcare Nutrition)"])
            uiform.select_multi_dropdown_item(label="Product", choice_label=["Finance"])
            uiform.select_multi_dropdown_item(label="Product",
                                              choice_label=["Finance", "Operating"])
            uiform.select_multi_dropdown_item(label="Product",
                                              choice_label=["Finance", "Operating",
                                                            "Master Hire (Current)"])
            uiform.select_multi_dropdown_item(label="Vehicle Type",
                                              choice_label=["Light Commercial"])
            uiform.select_multi_dropdown_item(label="Vehicle Type",
                                              choice_label=["Light Commercial", "Passenger"])
            uiform.select_multi_dropdown_item(label="Power Train",
                                              choice_label=["Hybrid Electric Vehicle"])
            uiform.select_multi_dropdown_item(label="Power Train",
                                              choice_label=["Hybrid Electric Vehicle",
                                                            "Internal Combustion Engine"])

        # vehicle‑utilisation
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting",
                                                page_name="vehicle-utilisation")
        if uiform:
            uiform.select_multi_dropdown_item(label="Country", choice_label=["Australia"])
            uiform.select_multi_dropdown_item(label="Country",
                                              choice_label=["Australia", "New Zealand"])
            uiform.select_multi_dropdown_item(label="Account Name",
                                              choice_label=["Nestle Australia Ltd (CPW)"])
            uiform.select_multi_dropdown_item(label="Account Name",
                                              choice_label=["Nestle Australia Ltd (CPW)",
                                                            "Nestle Australia Ltd (Healthcare Nutrition)"])
            uiform.select_multi_dropdown_item(label="Product", choice_label=["Finance"])
            uiform.select_multi_dropdown_item(label="Product",
                                              choice_label=["Finance", "Operating"])
            uiform.select_multi_dropdown_item(label="Product",
                                              choice_label=["Finance", "Operating",
                                                            "Used Vehicle Lease"])
            uiform.select_multi_dropdown_item(label="Vehicle Type",
                                              choice_label=["Light Commercial"])
            uiform.select_multi_dropdown_item(label="Vehicle Type",
                                              choice_label=["Light Commercial", "Passenger"])
            uiform.select_dropdown_item(label="Imminent Expiry",
                                        choice_label="Next 6 Months")
            uiform.select_multi_dropdown_item(label="Power Train",
                                              choice_label=["Hybrid Electric Vehicle"])

        # service‑overdue
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting",
                                                page_name="service-overdue")
        if uiform:
            uiform.select_multi_dropdown_item(label="Country", choice_label=["Australia"])
            uiform.select_multi_dropdown_item(label="Account Name",
                                              choice_label=["Nestle Australia Ltd (CPW)"])
            uiform.select_multi_dropdown_item(label="Product",
                                              choice_label=["Fleet Management"])
            uiform.select_multi_dropdown_item(label="Product",
                                              choice_label=["Fleet Management", "Operating"])
            uiform.select_dropdown_item(label="Overdue by", choice_label="Days")
            uiform.select_multi_dropdown_item(label="Vehicle Type",
                                              choice_label=["Passenger"])
            uiform.select_multi_dropdown_item(label="Power Train",
                                              choice_label=["Hybrid Electric Vehicle"])

        # # update‑profile
        # uiform = self.appian.visitor.visit_site(site_name="apac-reporting",
        #                                         page_name="update-profile")
        # if uiform:
        #     uiform.select_dropdown_item(label="Language",
        #                                 choice_label="English(UK)[en_GB]")
        #     uiform.click(label="SAVE")

        # manage-user and home
        self.appian.visitor.visit_site(site_name="apac-reporting", page_name="manage-user")
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting", page_name="home")
        if uiform:
            uiform.click(label="async-variable-refresh")

        # back to alerts and change language
        uiform = self.appian.visitor.visit_site(site_name="apac-reporting", page_name="alerts")
        # if uiform:
        #     uiform.select_dropdown_item(label="Language",
        #                                 choice_label="English(Australia)[en_AU]")


class UserActor(HttpUser):
    tasks = [GeneratedTaskSet]
    host = "https://orion-preprodanz.orix.com.au"
    auth = ["apac_nestle", "ORIX@2025"]
    wait_time = between(2, 5)
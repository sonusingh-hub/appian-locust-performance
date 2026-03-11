from core.base_page import BasePage
from core.ui_helpers import select_dropdown
from utils.waits import small_wait
import time


class HomePage(BasePage):

    def open(self):
        return self.visit(
            site_name="apac-reporting",
            page_name="home"
        )

    def open_vehicle_search(self, uiform):
        if not uiform:
            return None

        new_uiform = uiform.click(
            label="Vehicle Search"
        )
        small_wait()
        return new_uiform

    def select_country(self, uiform, country):
        if not uiform:
            return None

        new_uiform = select_dropdown(
            uiform,
            "Country",
            country
        )

        # extra wait so dependent picker values can load
        time.sleep(2)
        return new_uiform

    def fill_registration(self, uiform, value):
        if not uiform:
            return None

        # wait before interacting with picker
        time.sleep(1.5)

        try:
            new_uiform = uiform.fill_picker_field(
                label="test-Registration",
                value=value,
                format_test_label=False,
                identifier="#v"
            )
            small_wait()
            return new_uiform

        except Exception:
            # fallback: use shorter searchable prefix
            short_value = value.split(" - ")[0].strip()

            time.sleep(1)

            new_uiform = uiform.fill_picker_field(
                label="test-Registration",
                value=short_value,
                format_test_label=False,
                identifier="#v"
            )
            small_wait()
            return new_uiform

    def go_to_alerts(self):
        return self.visit(
            site_name="apac-reporting",
            page_name="alerts"
        )
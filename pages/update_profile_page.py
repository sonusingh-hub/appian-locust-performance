from core.base_page import BasePage
from core.ui_helpers import select_dropdown


class UpdateProfilePage(BasePage):

    def open(self):
        return self.visit(
            site_name="apac-reporting",
            page_name="update-profile"
        )

    def select_language(self, uiform, language):
        if not uiform:
            return None

        select_dropdown(
            uiform,
            "Language",
            language
        )
        return uiform
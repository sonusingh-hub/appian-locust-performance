from appian_locust import AppianTaskSet


class BaseJourney(AppianTaskSet):

    def on_start(self):
        super().on_start()

        if not hasattr(self, "user_context"):
            self.user_context = {}
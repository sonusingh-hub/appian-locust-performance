from locust import HttpUser, between
from journeys.smoke_analyst_journey import AnalystJourney


class OrionUser(HttpUser):
    host = "https://orion-testanz.orix.com.au"
    auth = ["TEST_PERF_PRIMARY", "ORIX@2026"]
    wait_time = between(2, 5)
    tasks = [AnalystJourney]
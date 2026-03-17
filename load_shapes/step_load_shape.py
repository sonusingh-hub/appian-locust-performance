import os
from locust import LoadTestShape


class StepLoadShape(LoadTestShape):
    """
    Dynamic step load shape based on scenario passed from PowerShell:
    $env:LOCUST_SCENARIO
    """

    scenario_stages = {
        "smoke": [
            {"duration": 40, "users": 2, "spawn_rate": 1},
            {"duration": 80, "users": 3, "spawn_rate": 1},
            {"duration": 120, "users": 5, "spawn_rate": 1},
        ],
        "smoke_10": [
            {"duration": 40, "users": 3, "spawn_rate": 1},
            {"duration": 80, "users": 5, "spawn_rate": 1},
            {"duration": 120, "users": 10, "spawn_rate": 2},
        ],
        "baseline_25": [
            {"duration": 40, "users": 5, "spawn_rate": 2},
            {"duration": 80, "users": 10, "spawn_rate": 2},
            {"duration": 120, "users": 25, "spawn_rate": 3},
        ],
        "baseline_50": [
            {"duration": 40, "users": 10, "spawn_rate": 2},
            {"duration": 80, "users": 25, "spawn_rate": 3},
            {"duration": 120, "users": 50, "spawn_rate": 5},
        ],
        "baseline_100": [
            {"duration": 40, "users": 20, "spawn_rate": 5},
            {"duration": 80, "users": 50, "spawn_rate": 5},
            {"duration": 120, "users": 100, "spawn_rate": 10},
        ],
        "standard": [
            {"duration": 40, "users": 50, "spawn_rate": 10},
            {"duration": 80, "users": 100, "spawn_rate": 10},
            {"duration": 120, "users": 200, "spawn_rate": 15},
        ],
        "peak": [
            {"duration": 120, "users": 100, "spawn_rate": 10},
            {"duration": 240, "users": 200, "spawn_rate": 10},
            {"duration": 360, "users": 300, "spawn_rate": 15},
        ],
        "stress400": [
            {"duration": 80, "users": 100, "spawn_rate": 10},
            {"duration": 160, "users": 200, "spawn_rate": 10},
            {"duration": 240, "users": 300, "spawn_rate": 15},
            {"duration": 300, "users": 400, "spawn_rate": 20},
        ],
        "stress500": [
            {"duration": 80, "users": 100, "spawn_rate": 10},
            {"duration": 160, "users": 200, "spawn_rate": 10},
            {"duration": 240, "users": 300, "spawn_rate": 15},
            {"duration": 320, "users": 400, "spawn_rate": 20},
            {"duration": 360, "users": 500, "spawn_rate": 20},
        ],
        "spike": [
            {"duration": 30, "users": 50, "spawn_rate": 25},
            {"duration": 60, "users": 150, "spawn_rate": 50},
            {"duration": 120, "users": 300, "spawn_rate": 100},
        ],
    }

    def tick(self):
        scenario = os.getenv("LOCUST_SCENARIO", "").strip()
        stages = self.scenario_stages.get(scenario)

        if not stages:
            return None

        run_time = self.get_run_time()

        for stage in stages:
            if run_time < stage["duration"]:
                return stage["users"], stage["spawn_rate"]

        return None
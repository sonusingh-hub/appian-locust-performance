import time
import random
import os


RUN_MODE_PROFILES = {
    "realistic": {
        "think": (0.5, 2.0),
        "small": (0.2, 0.7),
        "locust": (2.0, 5.0),
    },
    "balanced": {
        "think": (0.2, 1.0),
        "small": (0.1, 0.3),
        "locust": (1.0, 3.0),
    },
    "stress": {
        "think": (0.0, 0.2),
        "small": (0.0, 0.1),
        "locust": (0.1, 0.5),
    },
}

USER_BEHAVIOR_PROFILES = {
    "benchmark": {
        "abandonment_enabled": False,
        "reading_pause_scale": 0.15,
        "reading_pause_base": "small",
    },
    "realistic": {
        "abandonment_enabled": True,
        "reading_pause_scale": 1.0,
        "reading_pause_base": "think",
    },
}


def get_run_mode():
    mode = os.getenv("LOCUST_RUN_MODE", "realistic").strip().lower()
    return mode if mode in RUN_MODE_PROFILES else "realistic"


def get_user_behavior_profile():
    profile = os.getenv("LOCUST_USER_BEHAVIOR_PROFILE", "realistic").strip().lower()
    return profile if profile in USER_BEHAVIOR_PROFILES else "realistic"


def abandonment_enabled():
    return USER_BEHAVIOR_PROFILES[get_user_behavior_profile()]["abandonment_enabled"]


def get_locust_wait_range():
    profile = RUN_MODE_PROFILES[get_run_mode()]
    return profile["locust"]


def think_time(min_s=None, max_s=None):
    """Simulates real user thinking time."""
    if min_s is None or max_s is None:
        min_s, max_s = RUN_MODE_PROFILES[get_run_mode()]["think"]

    time.sleep(random.uniform(min_s, max_s))


def small_wait():
    min_s, max_s = RUN_MODE_PROFILES[get_run_mode()]["small"]
    time.sleep(random.uniform(min_s, max_s))


def reading_pause(rows=10):
    """Simulate the time a user spends scanning a data grid or result list.

    Applies a base think-time pause plus a small extra delay proportional to
    the expected number of visible rows. In benchmark mode the extra pause is
    heavily reduced so runs stay more repeatable.
    Caps additional delay at 1.5 s (for 50+ row grids).
    """
    behavior_profile = USER_BEHAVIOR_PROFILES[get_user_behavior_profile()]
    base_profile = behavior_profile["reading_pause_base"]
    min_s, max_s = RUN_MODE_PROFILES[get_run_mode()][base_profile]
    base = random.uniform(min_s, max_s)
    extra = min(rows / 50.0 * 1.5, 1.5) * behavior_profile["reading_pause_scale"]
    time.sleep(base + extra)
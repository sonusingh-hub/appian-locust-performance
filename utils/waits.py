import time
import random

def think_time(min_s=0.5, max_s=2.0):
    """Simulates real user thinking time."""
    time.sleep(random.uniform(min_s, max_s))


def small_wait():
    time.sleep(random.uniform(0.2, 0.7))
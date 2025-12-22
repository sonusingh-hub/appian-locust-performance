from locust import HttpUser, task, between, events, runners
from locust.runners import WorkerRunner
from appian_locust import AppianTaskSet

# requires the use of locust plugins and itertools
from locust_plugins.distributor import Distributor
import itertools

# Mock configuration with multiple credentials
# In a real scenario, this would usually be loaded from a JSON file
CONFIG = {
    "credentials": [
        ["user1", "pwd1"],
        ["user2", "pwd2"],
        ["user3", "pwd3"],
        ["user4", "pwd4"]
    ]
}

distributors = {}

@events.init.add_listener
def on_locust_init(environment, **_kwargs):
    user_iterator = None
    if not isinstance(environment.runner, WorkerRunner):
        # use itertools to cycle through the credentials, so that we wrap around at the end of the creds list.
        user_iterator = itertools.cycle(iter(CONFIG['credentials']))
    distributors["users"] = Distributor(environment, user_iterator, "users")

class DistributedTaskSet(AppianTaskSet):

    def on_start(self):
        self.parent.auth = next(distributors["users"])
        super().on_start()

    @task
    def print_current_user(self):
        print(f"Worker {self.workerId} running with user: {self.auth[0]}")

class UserActor(HttpUser):
    tasks = [DistributedTaskSet]
    wait_time = between(1, 2)
    host = "https://ml-test-old.load-test.appian-sites.net"

# To run use the following command:
# locust -f examples/example_distributed_creds.py --processes 4 --headless -u 7
# This will use 4 worker processes, with a total of 7 users, wrapping around the credentials list.
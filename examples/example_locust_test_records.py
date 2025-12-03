#!/usr/bin/env python3

import sys
import random

from locust import HttpUser, task, between

from appian_locust import AppianTaskSet
from appian_locust.utilities.loadDriverUtils import loadDriverUtils
from appian_locust.utilities import logger

# loadDriverUtils looks for a configuration file in your test's directory named 'config.json'.
# You can alter this behavior by passing your configuration file name into load_config. Eg: load_config(config_file='<your-config-file.json>')
utls = loadDriverUtils()
utls.load_config()
CONFIG = utls.c

logger = logger.getLogger(__file__)


class RecordsTaskSet(AppianTaskSet):

    def on_start(self):
        super().on_start()


        # could be either view or list:
        if "endpoint_type" not in CONFIG:	 # could be either view or list:
            logger.error("endpoint_type not found in config.json")
            sys.exit(1)

        self.endpoint_type = CONFIG["endpoint_type"]

        if "view" not in self.endpoint_type and "list" not in self.endpoint_type:
            logger.error(
                "This behavior is not defined for the provided endpoint type. Supported types are : view and list")
            sys.exit(1)
        # view = to view records from opaqueId
        # list = to list all the record types from url_stub

    def on_stop(self):
        logger.info("logging out")
        super().on_stop()

    @task(10)
    def visit_random_record(self):
        if "view" in self.endpoint_type:
            self.appian.visitor.visit_record_instance()

    @task(10)
    def visit_employee_record_type_list(self):
        if "list" in self.endpoint_type:
            record_list = self.appian.visitor.visit_record_type("Employees")
            record_list.filter_records_using_searchbox("Janet Coleman")

class RecordsUserActor(HttpUser):
    tasks = [RecordsTaskSet]

    # These determine how long each user waits between @task runs.
    # A random wait time will be chosen between min_wait and max_wait
    # for each task run, ie this script has no waiting by default.
    wait_time = between(0.500, 0.500)

    host = "https://" + CONFIG['host_address']
    auth = CONFIG["auth"]

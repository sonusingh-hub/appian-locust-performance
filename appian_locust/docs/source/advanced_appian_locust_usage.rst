.. _advanced_appian_locust_usage:

###################################
Advanced Appian Locust Usage
###################################

Loading Test Settings from Config
********************************************

These three lines look for a ``config.json`` file at the location from which the script is run (not where the locustfile is).

.. code-block:: python

    from appian_locust.utilities import loadDriverUtils

    utls = loadDriverUtils()
    utls.load_config()


This takes the content of the ``config.json`` file and places it into a variable as `utls.c`.
This allows us to access configurations required for logging in inside the class that extends HttpUser:

.. code-block:: python

    config = utls.c
    auth = config['auth']
    host = "https://" + config['host_address']


A minimal `config.json` looks like:

.. code-block:: json

    {
        "host_address": "site-name.appiancloud.com",
        "auth": [
            "user.name",
            "password"
        ]
    }

Multiple User Types with Different Credentials
*************************************************

You can create different types of users with different behaviors, credentials, and weights by defining multiple HttpUser classes. This is useful for simulating realistic user distributions where different user types have different access patterns.

A complete example can ge found here - `example_multi_user_locustfile.py <https://gitlab.com/appian-oss/appian-locust/-/blob/master/examples/example_multi_user_locustfile.py>`_.


.. code-block:: python

    class RegularUserTaskSet(AppianTaskSet):
        @task
        def browse_records(self):
            # Regular user workflow
            self.appian.visitor.visit_record_type(record_type="Employees")

    class ManagerUserTaskSet(AppianTaskSet):
        @task
        def manager_operations(self):
            # Manager-specific workflow with elevated permissions
            self.appian.visitor.visit_record_type(record_type="Departments")

    class RegularUserActor(HttpUser):
        """
        Regular users that interact with standard interfaces.
        Weight will be relative to all defined weights, 4 in this example.
        In this configuration we expect 3 regular users for every manager user.
        """
        tasks = [RegularUserTaskSet]
        host = f'https://{utls.c["host_address"]}'
        auth = utls.c["auth"][0]  # First auth entry
        wait_time = between(0.5, 1.0)
        weight = 3

    class ManagerUserActor(HttpUser):
        """
        Manager users with elevated privileges and different workflows.
        Weight will be relative to all defined weights, 4 in this example.
        In this configuration we expect 3 regular users for every manager user.
        """
        tasks = [ManagerUserTaskSet]
        host = f'https://{utls.c["host_address"]}'
        auth = utls.c["auth"][1]  # Second auth entry
        wait_time = between(1.0, 2.0)
        weight = 1

You can define multiple user credentials in a single ``config.json`` file:

.. code-block:: json

    {
        "host_address": "site-name.appiancloud.com",
        "auth": [
            ["regular.user", "password123"],
            ["manager.user", "managerpass456"]
        ]
    }

**Running**

When running this locustfile, it is important to note that the user count specified at runtime are evenly and sequentially spread across the HttpUsers. 
If you only specify one user to run when running locust, it will only choose one user actor to start:

.. code-block:: bash

    locust -f examples/example_multi_user_locustfile.py --headless -r 10 -t 3600 --users 1
    ...
    All users hatched: RegularUserActor: 1, ManagerUserActor: 0 (0 already running)


Make sure to run the locustfile with at least as many users as required by how you have the `weights <https://docs.locust.io/en/stable/writing-a-locustfile.html#weight-attribute>`_ configured for each HttpUser.

For the included sample, the weights are 3 and 1 respectively, meaning you'll have to spawn 4 users to get the ``ManagerUserActor`` to start up


.. code-block:: bash

    locust -f examples/example_multi_user_locustfile.py  --headless -r 10 -t 3600 --users 4
    ...
    All users hatched: RegularUserActor: 3, ManagerUserActor: 1 (0 already running)

Procedurally Generated Credentials
**********************************

For large-scale testing, you may find it convenient to procedurally generate user credentials instead of manually maintaining long lists. This is particularly useful when you need hundreds or thousands of test users with predictable naming patterns.

First, add these keys to your ``config.json``:

.. code-block:: json

    {
        "host_address": "site-name.appiancloud.com",
        "procedural_credentials_prefix": "testuser",
        "procedural_credentials_password": "testpassword123",
        "procedural_credentials_count": 100
    }

Then use the credential generation functions in your test script:

.. code-block:: python

    from locust import HttpUser, task
    from appian_locust import AppianTaskSet
    from appian_locust.utilities import loadDriverUtils
    from appian_locust.utilities.credentials import procedurally_generate_credentials, setup_distributed_creds

    utls = loadDriverUtils()
    utls.load_config()

    class YourTaskSet(AppianTaskSet):
        @task
        def your_workflow(self):
            # Your test workflow here
            self.appian.visitor.visit_record_type(record_type="Employees")

    class UserActor(HttpUser):
        tasks = [YourTaskSet]
        host = f'https://{utls.c["host_address"]}'

        # Generate credentials procedurally
        procedurally_generate_credentials(utls.c)

        # Set the generated credentials on the HttpUser
        credentials = utls.c["credentials"]

        # Alternatively set up distributed credentials for load testing (uncomment if running distributed)
        # this will ensure that credentials are evenly split across all locust instances.
        # credentials = setup_distributed_creds(utls.c)

**How it works:**

- ``procedural_credentials_prefix``: Base string for usernames (e.g., "testuser")
- ``procedural_credentials_count``: Number of users to generate (e.g., 100 creates testuser1, testuser2, ..., testuser100)
- ``procedural_credentials_password``: Password used for all generated users
- ``procedurally_generate_credentials()``: Creates the credential pairs and adds them to the config
- ``setup_distributed_creds()``: Distributes credentials across multiple load drivers in round-robin fashion when running in distributed mode

This approach is ideal for testing scenarios where you have many similar users with sequential naming patterns, and it automatically handles credential distribution across multiple load generators.

Request Duration Assertions
***************************

You can add timing assertions to ensure that specific operations complete within expected timeframes. This is useful for performance validation of a specific request, however see the warning below:

.. warning::
   We **strongly** recommend analyzing test results in *aggregate* after the test has completed, instead of making assertions like this during the actual test run. Individual request timing assertions are less reliable than analyzing percentiles (p50, p95, p99) across the entire test run, which provide better insights into overall system performance.

Add this context manager class to your test file:

.. code-block:: python

    import time
    from locust import events

    class time_assertion(object):
        def __init__(self, max_time, label="Operation"):
            self.max_time = max_time
            self.label = label

        def __enter__(self):
            self.start_time = time.perf_counter()
            return self

        def __exit__(self, exception_type, exception_value, traceback):
            self.end_time = time.perf_counter()
            execution_time = self.end_time - self.start_time

            if execution_time > self.max_time:
                # Log to Locust's request events for tracking
                events.request.fire(
                    request_type="Assertion",
                    name=f"Performance threshold exceeded: {self.label}",
                    response_time=execution_time * 1000,  # Convert to milliseconds
                    response_length=0,
                    response=None,
                    context=None,
                    exception=f"{self.label} - execution time exceeded the limit of {self.max_time}s"
                )

                # Also print to console for immediate visibility
                print(f"⚠️  {self.label} - execution time {execution_time:.4f}s exceeded the limit of {self.max_time}s")

Use it to wrap operations that should complete within a specific time:

.. code-block:: python

    @task
    def monitored_workflow(self):
        uiform = self.appian.visitor.visit_record_type(record_type="Employees")

        # Monitor performance but don't fail the test
        with time_assertion(1.0, "Record Navigation"):
            uiform = self.appian.visitor.visit_record_type(record_type="Orders")

        with time_assertion(0.5, "Button Interaction"):
            uiform.click_button("Create New", locust_request_label="[Records.Create] New Order")

##############
Debugging
##############

Oftentimes you will encounter errors or not get the appropriate load you expect when running tests.

Things you can use to get more information:

1. Add print statements to your Locust code or the installed ``appian-locust`` library
2. Inspect the output of the latencies that Locust periodically prints out, to see if certain requests are much slower than you expect
3. Verify using the browser console that the requests you are attempting to simulate match up with what Locust/appian-locust is sending
4. Setting the "record_mode" attribute to True on your HttpUser's ``client`` object will create a "recorded_responses"
   folder which will contain all requests and responses sent during test execution. You can do this in the ``__init__``
   method of your HttpUser, like so:

.. code-block:: python

    def __init__(self, environment) -> None:
        super().__init__(environment)
        self.client.record_mode = True

5. Use ``run_single_user`` from locust to debug using IDE breakpoints. Please refer https://docs.locust.io/en/stable/running-in-debugger.html
   for more details on run_single_user. For IDE settings, refer https://docs.google.com/document/d/18SsM_8tv9b3E3ciZ16wtnLFh3VbOW7EsTdsz77gUPZ0/edit?tab=t.0

.. code-block:: python

    from locust import run_single_user

    run_single_user(<UserActor>)


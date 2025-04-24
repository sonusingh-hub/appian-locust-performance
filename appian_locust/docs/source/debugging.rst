##############
Debugging
##############

Oftentimes you will encounter errors or not get the appropriate load you expect when running tests.

Things you can use to get more information:

1. Add print statements to your Locust code or the installed ``appian-locust`` library
2. Inspect the output of the latencies that Locust periodically prints out, to see if certain requests are much slower than you expect
3. Verify using the browser console that the requests you are attempting to simulate match up with what Locust/appian-locust is sending
4. Setting the "record_mode" attribute to True on your HttpUser's or AppianTaskSequence's ``client`` object will create a "recorded_responses"
   folder which will contain all requests and responses sent during test execution. You can also set the "record_mode" attribute to True on 
   an AppianTaskSet's ``appian.interactor`` object. You can do this in the ``__init__`` method of your HttpUser, like so:

.. code-block:: python
    
    class MyClass(HttpUser):

        def __init__(self, environment) -> None:
            super().__init__(environment)
            self.client.record_mode = True

        @task
        def do_something(self):
            #create request here

5. Use ``run_single_user`` from locust to debug using IDE breakpoints. Please refer https://docs.locust.io/en/stable/running-in-debugger.html
   for more details on run_single_user.

.. code-block:: python

    from locust import run_single_user

    run_single_user(<UserActor>)


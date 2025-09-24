##############
Debugging
##############

When you encounter errors or unexpected behavior during testing, Appian Locust provides several debugging tools and techniques to help identify and resolve issues.

Initial Troubleshooting Steps
*****************************

- **Start simple:** Test with a single user before scaling up to multiple users
- **Use print statements** strategically throughout your test code
- **Verify your test environment** is accessible and functioning normally before load testing
- **Check Locust's web UI** for detailed request statistics and failure information
- **Monitor system resources** (CPU, memory) during test execution to identify bottlenecks

Request and Response Recording
******************************

Enable detailed recording of all HTTP requests and responses to inspect what's being sent to your Appian instance.

**Enable recording in your test:**

.. code-block:: python

    class YourTaskSet(AppianTaskSet):

        def __init__(self, parent):
            super().__init__(parent)
            self.client.record_mode = True

        @task
        def your_test(self):
            # Your test code here
            pass


When enabled, all requests and responses will be saved in a ``recorded_responses`` folder where your test runs. Each file contains the full HTTP request and response data for inspection. In addition on an Appian Cloud system a trace ID will be printed out that can be shared with Appian Support for investigation.



Common Debugging Scenarios
***************************

**Monitoring the execution:**

Locust periodically prints latency statistics to the console. Look for:

- Requests that are much slower than expected
- High failure rates for specific operations
- Review the locust logs for exceptions
- Request trends over time

**Debugging UI State:**

.. code-block:: python

    import json

    # Add this to see the current page state
    @task
    def debug_page_state(self):
        uiform = self.appian.visitor.visit_record_type("YourRecord")
        print(f"Current page components: {uiform._state}")

        # Alternatively, write it to a file for easier inspection
        with open('page_state.json', 'w') as f:
            f.write(json.dumps(uiform._state, indent=2))



**Increase logging verbosity:**

Leverage Locust's built in `logging options <https://docs.locust.io/en/stable/logging.html#options>`__.

.. code-block:: bash

    locust -f your_test.py --loglevel DEBUG


Browser Comparison
******************

Compare your Appian Locust requests with actual browser behavior:

1. **Open browser developer tools** (F12) and go to the Network tab
2. **Perform the same actions** manually in your browser
3. **Compare the requests** that Appian Locust sends with what the browser sends
4. **Look for differences** in requests and the payloads.
5. **Ensure responses look relevant** for the components the test is trying to interact with


Single-User Debug Mode
**********************

Run your tests in single-user mode to use IDE breakpoints and step through your code line by line.

.. code-block:: python

    from locust import run_single_user
    from your_test_file import YourUserActor

    # Run a single user for debugging
    run_single_user(YourUserActor)

This allows you to:

- Set breakpoints in your IDE
- Step through test execution
- Inspect variables and state
- Debug complex workflows interactively

For more details, see the `Locust debugging documentation <https://docs.locust.io/en/stable/running-in-debugger.html>`__.



Getting Help
************

If you're still experiencing issues after trying these debugging techniques:

- Check the `Gitlab Issues <https://gitlab.com/appian-oss/appian-locust/-/issues>`__ for similar problems, create a new issue if you don't find anything.
- Review the `full documentation <https://appian-locust.readthedocs.io/en/latest/>`__ for additional guidance
- Did you fix your issue? Consider suggesting improvements to our docs!



##############
Debugging
##############

Oftentimes you will encounter errors or not get the appropriate load you expect when running tests.

Things you can use to get more information:

1. Add print statements to your Locust code or the installed ``appian-locust`` library
2. Inspect the output of the latencies that Locust periodically prints out, to see if certain requests are much slower than you expect
3. Verify using the browser console that the requests you are attempting to simulate match up with what Locust/appian-locust is sending
4. Setting the "record_mode" attribute to True on your HttpUser will create a "recorded_responses"
   folder which will contain all requests and responses sent during test execution.

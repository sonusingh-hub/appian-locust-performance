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
    auth = utls.c['auth']


A minimal `config.json` looks like:

.. code-block:: json

    {
        "host_address": "site-name.appiancloud.com",
        "auth": [
            "user.name",
            "password"
        ]
    }


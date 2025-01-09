##############
User Agents
##############

Appian Locust will use the following user agent strings for requests against the specified hostname:

Desktop: ``Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36``
Mobile: ``Mozilla/5.0 (Android 15; Mobile; rv:68.0) Gecko/68.0 Firefox/134.0``

To override these user agents, you can defined them like so:

.. code-block:: python

    def __init__(self, environment) -> None:
        super().__init__(environment)
        self.client.user_agent_desktop = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        self.client.user_agent_mobile = "Mozilla/5.0 (Android 15; Mobile; rv:68.0) Gecko/68.0 Firefox/134.0"

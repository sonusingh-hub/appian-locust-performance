.. include:: ../../../README.rst
    :start-after: what_is_appian_locust-inclusion-begin-do-not-remove
    :end-before: what_is_appian_locust-inclusion-end-do-not-remove

What is Locust?
_________________________________

It’s an open source python library for doing load testing (think `JMeter <https://jmeter.apache.org/>`_, but in Python).
It is by default HTTP-driven, but can be made to work with other types of interactions.
Visit `Locust <https://docs.locust.io/en/stable/>`__ for more information.

Locust has the benefit of relying purely on API requests, which makes it lower overhead than frameworks building
on Selenium or browser automation libraries. We have also found python to be common denominator across software and quality engineers,
making it a convenient language for extending the framework and defining tests.
Using Locust's model of ``TaskSets`` and ``TaskSequences``, it is easy to compose user operations in a maintainable way.
Appian-Locust builds on these concepts by defining :class:`.AppianTaskSet` and :class:`.AppianTaskSequence`, which layer on Appian-specific
functionality such as login and session management.


SAIL Navigation
_________________________________


Appian interfaces are built with `SAIL <https://docs.appian.com/suite/help/latest/SAIL_Design.html>`__.
It's a RESTful contract that controls state between the browser/mobile clients and the server.

All SAIL-based interactions require updating a server-side context (or in a stateless mode, passing that context back and forth).
These updates are expressed as JSON requests sent back and forth, which are sent as "SaveRequests", usually to the same endpoint from which the original SAIL form was served. Each SaveRequest, if successful, will return an updated component, or a completely new form if a modal is opened or a button is clicked on a wizard.

Appian Locust abstracts away the specifics of these requests into methods that make it easy to quickly create new workflows for Locust's virtual users to execute on an Appian instance,
For more details on how Appian Locust enables this, check out the :ref:`how_to_write_locust_tests` section.

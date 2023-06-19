##############
Release Notes
##############
.. release-notes-latest-inclusion-begin-do-not-remove
Version 2.0.0
=============

Enhancements
------------

TBD - see migration guide here <TBD>

Features
--------
* Metadata for News, Tasks, Records, Reports, Actions, and Sites can be fetched from :class:`~appian_locust.appian_client.AppianClient`.


Breaking Changes
----------------

* Appian Locust now requires Python 3.10. Update your dependencies globally or within your dependency management config file.
* :class:`~appian_locust.uiform.uiform.SailUiForm` interactions are now conducted through :class:`~appian_locust.visitor.Visitor`.
* Non UI form interactions at the system level are conducted through :class:`~appian_locust.system_operator.SystemOperator` (i.e. :meth:`~appian_locust.system_operator.SystemOperator.get_webapi`).
* :meth:`~appian_locust.utilities.loadDriverUtils.loadDriverUtils` does not provide ``utls`` anymore. Instead, call :meth:`~appian_locust.utilities.loadDriverUtils.loadDriverUtils` to set ``utls``:

    .. code-block:: python

        from appian_locust.utilities import loadDriverUtils
        utls = loadDriverUtils()

.. release-notes-latest-inclusion-end-do-not-remove

##############
Release Notes
##############
.. release-notes-latest-inclusion-begin-do-not-remove
Version 2.0.0
=============

Appian Locust v2.0 introduces a significant rework of the API to guide a clear and streamlined development experience. Our target was to meet feature parity while simplifying the steps to interact with Appian.

New Paradigm
------------
* :class:`~appian_locust.visitor.Visitor` is the new hub for all SailUiForm navigations. From the client, you can call various methods to retrieve the desired :class:`~appian_client.uiform.SailUiForm` that matches the type of page that the caller has navigated to, which will enable further interaction with the represented UI.
* :class:`~appian_locust.system_operator.SystemOperator` is for non UI form interactions at the system level (i.e. :meth:`~appian_locust.system_operator.SystemOperator.get_webapi`).
* The :mod:`~appian_locust.info` module extended from :class:`~appian_locust.appian_client.AppianClient` provides metadata for News, Tasks, Records, Reports, Actions, and Sites (i.e. :attr:`appian_locust.appian_client.AppianClient.actions_info`).


Breaking Changes
----------------

* Appian Locust now requires Python 3.10. Update your dependencies globally or within your dependency management config file.
* Fetching SailUIForms from News, Tasks, Records, Reports, Actions, and Sites have been marked as private. Use :class:`~appian_locust.visitor.Visitor` to handle all UI navigations.
* SailUIForms types can be found in the :mod:`~appian_locust.uiform` module.
* Design objects and types have been moved to the :mod:`~appian_locust.objects` module.
* Various helper methods have been moved to the :mod:`~appian_locust.utilities` module.
* :meth:`~appian_locust.utilities.loadDriverUtils.loadDriverUtils` does not provide ``utls`` anymore. Instead, call :meth:`~appian_locust.utilities.loadDriverUtils.loadDriverUtils` to set ``utls``:

    .. code-block:: python

        from appian_locust.utilities import loadDriverUtils
        utls = loadDriverUtils()

For a more comprehensive list of changes in Appian Locust 2.0, see the :ref:`v2_upgrade` document.

.. release-notes-latest-inclusion-end-do-not-remove

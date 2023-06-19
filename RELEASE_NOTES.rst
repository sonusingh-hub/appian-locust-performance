##############
Release Notes
##############
.. release-notes-latest-inclusion-begin-do-not-remove
Version 2.0.0
=============

Enhancements
------------

TBD - see migration guide here <TBD>

Breaking Changes
----------------

* ``loadDriverUtils`` does not provide ``utls`` anymore. Instead, call ``loadDriverUtils`` to set any variables called ``utls``:
    .. code-block:: python

        from appian_locust.utilities import loadDriverUtils
        utls = loadDriverUtils()

.. release-notes-latest-inclusion-end-do-not-remove

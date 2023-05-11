.. note::
    By contributing to this Open Source project, you provide Appian Corporation a non-exclusive, perpetual, royalty-free license to use your contribution for any purpose.

********************
Contributing
********************

#. Fork the `appian-locust <https://gitlab.com/appian-oss/appian-locust>`__ repository
#. Make any desired changes
#. Commit changes and push to your fork
#. Make a merge request to the upstream fork and project maintainers will review it

New Development
---------------
As new development is done to Appian Locust, the core principle of user navigation and resulting interaction should be kept in mind.
Is your feature adding interaction capabilities to an existing type of page? If so, you likely want to add a new method to an
existing ``SailUiForm`` type. Otherwise, you might need to create a new extention of ``SailUiForm`` and ensure that the ``Visitor``
class has the capabilities to visit the new page type. Lastly, functionality that doesn’t involve user interaction should be included in the
``SiteHelper`` class.

If you think that your development falls outside of the above criteria, you should submit an issue for the maintainers of this project
to discuss your use case.

To Test Your Changes
--------------------
In any test-implementation repo where you use appian-locust, change the following (assuming you're using a ``Pipfile``)

.. code-block:: python

    appian-locust = {path="../appian-locust", editable=true}

**NOTE** The path above assumes appian-locust is checked out locally, hence we can use a relative directory path.

And run ``pipenv install --skip-lock`` to allow you to use a local version of appian-locust
without recreating the lock file. However, remember to use a lock file in your test-implementation repo.

Now you can test your changes as you normally would.

Internal Classes
----------------
Apart from our exposed API, we provide `internal classes <https://gitlab.com/appian-oss/appian-locust/appian_locust>`__ for more granular control when developing or testing.

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
class has the capabilities to visit the new page type. Lastly, functionality that doesn't involve user interaction should be included in the
``SiteHelper`` class.

If you think that your development falls outside of the above criteria, you should submit an issue for the maintainers of this project
to discuss your use case.

To Test Your Changes
--------------------
In any test-implementation repo where you use appian-locust, change the following (assuming you're using a ``Pipfile``)

.. code-block:: python

    appian-locust = {path="../appian-locust", editable=true}

By supplying a local repository path pointing to your local appian-locust repo, you can modify appian-locust and observe changes in realtime.

And run ``pipenv install --skip-lock`` to allow you to use a local version of appian-locust
without recreating the lock file. However, remember to use a lock file in your test-implementation repo.

PyCharm Setup:
--------------

1. Open PyCharm Settings
2. Select Project: <your-project>
3. Select Python Interpreter
4. Click the dropdown and select 'Show All'
5. Click the tree icon in the sidebar
6. Click the plus icon, navigate to your local appian-locust repository, and click OK all the way through

VSCode Setup:
-------------

1. Open control palette (Cmd + Shift + P)
2. Select Preferences: Open Workspace Settings (JSON)
3. Add the following snippet

.. code-block:: JSON

    {
        "python.analysis.extraPaths": ["<absolute-path-to>/appian-locust"],
    }

Now you can test your changes as you normally would.

Internal Classes
----------------
Apart from our exposed API, we provide `internal classes <https://gitlab.com/appian-oss/appian-locust/appian_locust>`__ for more granular control when developing or testing.

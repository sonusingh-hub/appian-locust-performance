.. what_is_appian_locust-inclusion-begin-do-not-remove

#######################################
What is Appian Locust?
#######################################

Appian Locust is a wrapper library around `Locust <https://locust.io>`__ for load testing Appian.
This library is intended to be used as an alternative to tools such as Jmeter and Load Runner.

Appian Locust capabilities

- Logging in and logging out
- Form interactions (filling/submitting)
- Finding and interacting with basic components on a SAIL interface
- Navigating to records/reports/sites

.. what_is_appian_locust-inclusion-end-do-not-remove


For full documentation, visit the `docs page <https://appian-locust.readthedocs.io/en/latest/>`__.

.. disclaimer-inclusion-begin-do-not-remove

**Disclaimer:**
This library is continuously evolving.
Currently the main focus is supporting essential use-cases.
We are happy to accept contributions to further extend functionality, address bug fixes and improve usability.
Please see the `Contributing <https://appian-locust.readthedocs.io/en/latest/contributing.html>`__ section and feel free to reach out.

.. disclaimer-inclusion-end-do-not-remove

.. quick_start-inclusion-begin-do-not-remove

************************
Quick Installation Guide
************************

This guide helps you get up and running with the ``appian-locust`` library quickly.

We strongly recommend using ``pipenv`` and ``pyenv`` to automatically manage Python versions and environments. This ensures a clean and reproducible setup for running and developing tests with Locust.

.. note::
  💡 If you don’t want to manage environments manually, jump to the *Automatic Setup* section below.

Manual Setup
------------

1. Install appian-locust using ``pip``, for more comprehensive projects we recommend using ``pipenv``.

.. code-block:: bash

      pip install appian-locust


If using ``pipenv``, simply start from the following ``Pipfile``:

.. code-block:: toml

    [packages]
    appian-locust = {version = "*"}

    [requires]
    python_version = "3.13"

Build from source
----------------------
1. Clone the repository:

.. code-block:: bash

    git clone -o prod git@gitlab.com:appian-oss/appian-locust.git


2a. Install the library globally:

.. code-block:: bash

    pip install -e appian-locust


2b. Or within a virtual environment:

.. code-block:: bash

    pipenv install -e appian-locust

Note: It’s highly recommended that you use a virtual environment when installing python artifacts. You can follow the instructions `here <https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/>`__ to install virtualenv and pip.

If you have issues installing, make sure you have the proper prerequisites installed for Locust and its dependencies.
If you're having trouble on Windows, check `here <https://github.com/locustio/locust/issues/1208#issuecomment-569693439>`__

Automatic Setup
---------------

To simplify the setup process and avoid installing Python manually, use the provided `setup.sh <https://gitlab.com/appian-oss/appian-locust/-/blob/main/setup.sh>`__ script. It will:

- Install ``pyenv`` and ``pipenv`` if they are missing.
- Install the correct Python version from the ``Pipfile``.
- Create a virtual environment.
- Install all dependencies.

1. Clone the repository:

.. code-block:: bash

    git clone -o prod git@gitlab.com:appian-oss/appian-locust.git


2. Navigate to `appian-locust` directory and make the script `setup.sh` executable:

.. code-block:: bash

    cd appian-locust/
    chmod +x setup.sh

3. Run the setup:

.. code-block:: bash

    ./setup.sh

4. After setup, activate the virtual environment:

.. code-block:: bash

    pipenv shell


Test environment setup
----------------------
Download the sample test `example_locustfile.py <https://gitlab.com/appian-oss/appian-locust/-/blob/main/examples/example_locustfile.py>`__ from the Appian Locust repo and run it.

.. code-block:: bash

    locust -f example_locustfile.py

If everything is set up correctly, you should see a link to the `Locust web interface <https://docs.locust.io/en/stable/quickstart.html#locust-s-web-interface>`__, which you can use to start test runs and view results.

* For more information about how to build the workflow for your locust test, see the `How to Write a Locust Test <https://appian-locust.readthedocs.io/en/latest/how_to_write_locust_tests.html>`__ section.

``appian-locust`` should now be ready to run your Locust performance tests!

Consolidated Client Report (PowerShell Runner)
----------------------------------------------

If you are using ``run_tests.ps1`` and want a single client-facing PDF that consolidates recent scenario runs, use the ``-generateClientReport`` switch.

Example:

.. code-block:: powershell

  .\run_tests.ps1 -scenario baseline_50 -env TEST -reportMode full -generateClientReport

Outputs:

- Per-run artifacts are generated in the scenario result folder (for example ``results\baseline_50_<timestamp>``).
- Consolidated report is generated at ``results\apac_performance_report.pdf``.

Notes:

- The consolidated report is built from discovered scenario result folders containing ``*_stats.csv``.
- By default, the latest 5 runs are included globally.

PowerShell Runner Command Reference
-----------------------------------

The framework runner is ``run_tests.ps1``.

Base syntax:

.. code-block:: powershell

  .\run_tests.ps1 -scenario <scenario> [options]

Supported scenarios:

- ``smoke``
- ``smoke_10``
- ``baseline_25``
- ``baseline_50``
- ``baseline_100``
- ``standard``
- ``peak``
- ``stress400``
- ``stress500``
- ``spike``

Supported option values:

- ``-env``: ``TEST`` | ``PRE-PROD``
- ``-executionMode``: ``normal`` | ``step``
- ``-logLevel``: ``DEBUG`` | ``INFO`` | ``WARNING`` | ``ERROR`` | ``CRITICAL``
- ``-runMode``: ``realistic`` | ``balanced`` | ``stress``
- ``-userBehaviorProfile``: ``benchmark`` | ``realistic``
- ``-credentialMode``: ``auto`` | ``reserved`` | ``reserve`` | ``reuse``
- ``-reportMode``: ``off`` | ``minimal`` | ``full``
- ``-outlierThresholdMs``: numeric value (default ``120000``)
- ``-collectFullHistory``: switch
- ``-generateClientReport``: switch

Scenario command examples:

.. code-block:: powershell

  .\run_tests.ps1 -scenario smoke
  .\run_tests.ps1 -scenario smoke_10
  .\run_tests.ps1 -scenario baseline_25
  .\run_tests.ps1 -scenario baseline_50
  .\run_tests.ps1 -scenario baseline_100
  .\run_tests.ps1 -scenario standard
  .\run_tests.ps1 -scenario peak
  .\run_tests.ps1 -scenario stress400
  .\run_tests.ps1 -scenario stress500
  .\run_tests.ps1 -scenario spike

Common combinations:

.. code-block:: powershell

  # Full reports (HTML + PDF)
  .\run_tests.ps1 -scenario baseline_50 -env TEST -reportMode full

  # PDF-only report
  .\run_tests.ps1 -scenario baseline_25 -reportMode minimal

  # Disable report generation
  .\run_tests.ps1 -scenario smoke_10 -reportMode off

  # Step load-shape execution
  .\run_tests.ps1 -scenario baseline_50 -executionMode step

  # Benchmark behavior profile
  .\run_tests.ps1 -scenario baseline_50 -userBehaviorProfile benchmark

  # Explicit credential reuse
  .\run_tests.ps1 -scenario baseline_50 -credentialMode reuse

  # Include full Locust history CSV
  .\run_tests.ps1 -scenario baseline_50 -collectFullHistory

  # Full run + consolidated client report
  .\run_tests.ps1 -scenario baseline_50 -env TEST -reportMode full -generateClientReport

Consolidated report only (from existing results folders):

.. code-block:: powershell

  .\.venv\Scripts\python.exe scripts\generate_client_report.py --results-root results --output results\apac_performance_report.pdf --max-runs 5

Consolidated report examples (scenario filters and latest-N):

.. code-block:: powershell

  # Latest 3 runs only from baseline/smoke/baseline_25
  .\.venv\Scripts\python.exe scripts\generate_client_report.py --results-root results --scenarios baseline smoke baseline_25 --max-runs 3

  # Same as above using comma-separated scenario filters
  .\.venv\Scripts\python.exe scripts\generate_client_report.py --results-root results --scenarios baseline,smoke,baseline_25 --max-runs 3

  # Latest 2 runs globally from any scenario category
  .\.venv\Scripts\python.exe scripts\generate_client_report.py --results-root results --max-runs 2

Troubleshooting
----------------

Installation Issues
^^^^^^^^^^^^^^^^^^^

* **Permissions issue when cloning appian-locust**

  * Ensure you have added your SSH key to your GitLab profile. See `here <https://docs.gitlab.com/ee/user/ssh.html#add-an-ssh-key-to-your-gitlab-account>`__ for instructions.
  * Alternatively, download the `ZIP bundle <https://gitlab.com/appian-oss/appian-locust/-/archive/main/appian-locust-main.zip>`__.

* **"locust is not available" or "command not found"**

  * Verify you ran ``pip install appian-locust``
  * If using a virtual environment, ensure it's activated: ``pipenv shell``
  * Check your PATH includes the Python or Pyenv directory

  .. code-block:: bash

    echo $PATH | grep -e "python" -e "pyenv"

* **Python version compatibility errors**

  * Appian Locust requires Python 3.13+. Check your version: ``python --version``
  * Consider using ``pyenv`` to manage multiple Python versions


Connection & Authentication Issues
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* **"Failed to establish a new connection: [Errno 8] nodename nor servname provided, or not known"**

  * Verify ``host_address`` in your config.json is correct (without https://)
  * If behind a corporate firewall, check any network security tools like ZScaler or any outbound proxy settings.

* **"Login unsuccessful, no multipart cookie found"**

  * Verify username and password in ``auth`` are correct for your Appian site
  * Verify the user has appropriate permissions to access the site, try in a browser

* **SSL/Certificate errors**

  * For self-signed certificates you may need to disable SSL verification, but make sure you actually trust the host you are testing against.

  .. code-block:: python

      class UserActor(HttpUser):
          def on_start(self):
              self.client.verify = False


Runtime Issues
^^^^^^^^^^^^^^^^^^

* **Tests run but no interactions complete**

  * Verify that your Appian site is accessible in a browser
  * Ensure your test users have access to the interfaces you're testing


Need More Help?
-------------------

* For detailed debugging techniques, request recording, and advanced troubleshooting, see the `Debugging Guide <https://appian-locust.readthedocs.io/en/latest/debugging.html>`__

.. quick_start-inclusion-end-do-not-remove

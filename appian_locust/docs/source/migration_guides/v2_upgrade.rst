.. _v2_upgrade:

*********************************************************************
Appian Locust 2.0 Migration Guide
*********************************************************************

_actions.py
===========
The _Actions class is no longer available. You may migrate any functionality using this class as follows:

.. list-table::
   :widths: 20 40 40
   :header-rows: 1

   * - Method in 1.x
     - Method in 2.x
     - Example Usage
   * - get_actions_interface
     - Not available anymore. Handled internally by the framework whenever it is necessary, so any calls to this can be removed without replacement.
     -
   * - get_actions_feed
     - Not available anymore. Handled internally by the framework whenever it is necessary, so any calls to this can be removed without replacement.
     -
   * - get_all
     - We can do the same operation from the actions_info.py method named “get_all_available_actions”.
     - all_available_actions = :meth:`self.appian.actions_info.get_all_available_actions(..)<appian_locust.info.actions_info.ActionsInfo.get_all_available_actions>`
   * - get_action
     - We can do the same operation from the actions_info.py method named “get_action_info”.
     - specific_action_info =  :meth:`self.appian.actions_info.get_action_info(..)<appian_locust.info.actions_info.ActionsInfo.get_action_info>`
   * - visit_and_get_form
     - We can perform the same operation by the “visit_action” method from visitor.py.
     - uiform = :meth:`self.appian.visitor.visit_action(..)<appian_locust.visitor.Visitor.visit_action>`
   * - visit
     - Not available. Call the “visit_action” method from visitor.py instead.
     - uiform = :meth:`self.appian.visitor.visit_action(..)<appian_locust.visitor.Visitor.visit_action>`
   * - start_action
     - We can perform the same operation by calling “start_action” in system_operator.py
     - response = :meth:`self.system_operator.start_action(...)<appian_locust.system_operator.SystemOperator.start_action>`

_admin.py
=========
The _Admin class is no longer available. You may migrate any functionality using this class as follows:

.. list-table::
   :widths: 20 40 40
   :header-rows: 1

   * - Method in 1.x
     - Method in 2.x
     - Example Usage
   * - visit
     - We can do the same operation by calling “visit_admin” method in visitor.py
     - uiform = :meth:`self.appian.visitor.visit_admin()<appian_locust.visitor.Visitor.visit_admin>`

_design.py
==========
The _Design class is no longer available. You may migrate any functionality using this class as follows:

.. list-table::
   :widths: 20 40 40
   :header-rows: 1

   * - Method in 1.x
     - Method in 2.x
     - Example Usage
   * - visit
     - We can do the same operation by calling “visit_design” method in visitor.py
     - uiform = :meth:`self.appian.visitor.visit_design()<appian_locust.visitor.Visitor.visit_design>`
   * - visit_object
     - We can do the same operation by calling “visit_design_object_by_id” method in visitor.py
     - design_object_uiform = :meth:`self.appian.visitor.visit_design_object_by_id(..)<appian_locust.visitor.Visitor.visit_design_objecT_by_id>`
   * - visit_app
     - We can do the same operation by calling “visit_application_by_id” method in visitor.py
     - application_uiform = :meth:`self.appian.visitor.visit_application_by_id(..)<appian_locust.visitor.Visitor.visit_application_by_id>`
   * - create_application
     - We can do the same operation by calling “create_application” method in design_uiform.py
     - | design_uiform = self.appian.visit_design()
       | application_uiform = :meth:`design_uiform.create_application(..)<appian_locust.uiform.design_uiform.DesignUiForm.create_application>`
   * - create_record_type
     - We can do the same operation by calling “create_record_type” method in application_uiform.py
     - | application_uiform = self.appian.visitor.visit_application_by_id(..)
       | application_uiform = :meth:`application_uiform.create_record_type(..)<appian_locust.uiform.application_uiform.ApplicationUiForm.create_record_type>`
   * - create_report
     - We can do the same operation by calling “create_recport” method in application_uiform.py
     - | application_uiform = self.appian.visitor.visit_application_by_id(..)
       | application_uiform = :meth:`application_uiform.create_report(..)<appian_locust.uiform.application_uiform.ApplicationUiForm.create_report>`

_news.py
========
The _News class is no longer available. You may migrate any functionality using this class as follows:

.. list-table::
   :widths: 20 40 40
   :header-rows: 1

   * - Method in 1.x
     - Method in 2.x
     - Example Usage
   * - get_all
     - We can do the same operation by calling the “get_all_available_entries” method in news_info.py.
     - news_dict = :meth:`self.appian.news_info.get_all_available_entries(..)<appian_locust.info.news_info.NewsInfo.get_all_available_entries>`
   * - get_news
     - We can do the same operation by calling the “get_news_entry” method in news_info.py.
     - specific_news_info = :meth:`self.appian.news_info.get_news_entry(..)<appian_locust.info.news_info.NewsInfo.get_news_entry>`
   * - visit
     - Not available. Call “get_news_entry” method in news_info.py instead.
     - specific_news_info = :meth:`self.appian.news_info.get_news_entry(..)<appian_locust.info.news_info.NewsInfo.get_news_entry>`
   * - visit_news_entry
     - Not available. Call “get_news_entry” method in news_info.py instead.
     - specific_news_info = :meth:`self.appian.news_info.get_news_entry(..)<appian_locust.info.news_info.NewsInfo.get_news_entry>`
   * - search
     - We can do the same operation by calling the “get_all_available_entries” with a search string argument.
     - uiform = :meth:`self.appian.news_info.get_all_available_entries(..)<appian_locust.info.news_info.NewsInfo.get_all_available_entries>`

_records.py
===========
The _Records class is no longer available. You may migrate any functionality using this class as follows:

.. list-table::
   :widths: 20 40 40
   :header-rows: 1

   * - Method in 1.x
     - Method in 2.x
     - Example Usage
   * - visit_record_instance_and_get_feed_form
     - Not available. Call “visit_record_instance” method in visitor.py instead.
     - record_instance_uiform = :meth:`self.appian.visitor.visit_record_instance(..)<appian_locust.visitor.Visitor.visit_record_instance>`
   * - visit_record_instance_and_get_form
     - We can do the same operation by calling the “visit_record_instance” method in visitor.py
     - record_instance_uiform = :meth:`self.appian.visitor.visit_record_instance(..)<appian_locust.visitor.Visitor.visit_record_instance>`
   * - visit_record_type_and_get_form
     - We can do the same operation by calling the  “visit_record_type” method in visitor.py
     - record_list_uiform = :meth:`self.appian.visitor.visit_record_type(..)<appian_locust.visitor.Visitor.visit_record_type>`
   * - get_all
     - We can do the same operation from the record_list_uiform.py method named “get_visible_record_instances”.
     - | record_list_uiform = self.appian.visitor.visit_record_type(..)
       | all_records_info = :meth:`record_list_uiform.get_visible_record_instances(..)<appian_locust.uiform.records_list_uiform.RecordsListUiForm.get_visible_record_instances>`
   * - get_all_record_types
     - “get_all_available_record_types” in records_info.py
     - records_dict = :meth:`self.appian.records_info.get_all_available_record_types(..)<appian_locust.info.records_info.RecordsInfo.get_all_available_record_types>`
   * - get_all_records_of_record_type
     - “get_visible_record_instances” in record_list_uiform.py
     - | record_list_uiform = self.appian.visitor.visit_record_type(..)
       | all_records_info = :meth:`record_list_uiform.get_visible_record_instances(..)<appian_locust.uiform.records_list_uiform.RecordsListUiForm.get_visible_record_instances>`
   * - get_records_interface
     - Not available. Handled internally by the framework whenever it is necessary, so any calls to this can be removed without replacement.
     -
   * - get_records_nav
     - Not available. Handled internally by the framework whenever it is necessary, so any calls to this can be removed without replacement.
     -
   * - get_all_records_of_record_type_mobile
     - To interact with an Appian instance as a mobile client, pass in “is_mobile_client=True” in the AppianTaskSet on_start method.
     - | class SampleTaskSet(AppianTaskSet)
       |    def on_start(self):
       |    super().on_start(is_mobile_client=True)
   * - get_all_mobile
     - To interact with an Appian instance as a mobile client, pass in “is_mobile_client=True” in the AppianTaskSet on_start method.
     - | class SampleTaskSet(AppianTaskSet)
       |    def on_start(self):
       |    super().on_start(is_mobile_client=True)
   * - fetch_record_instance
     - Not available. Instead call “visit_record_instance” method in visitor.py
     - record_instance_uiform = :meth:`self.appian.visitor.visit_record_instance(..)<appian_locust.visitor.Visitor.visit_record_instance>`
   * - fetch_record_type
     - Not available. Instead call “visit_record_type” method in visitor.py
     - record_list_uiform = :meth:`self.appian.visitor.visit_record_type(..)<appian_locust.visitor.Visitor.visit_record_type>`
   * - visit_record_instance
     - Not available. Instead call “visit_record_instance” method in visitor.py
     - record_instance_uiform = :meth:`self.appian.visitor.visit_record_instance(..)<appian_locust.visitor.Visitor.visit_record_instance>`
   * - visit_record_type
     - Not available. Instead call “visit_record_type” method in visitor.py
     - record_list_uiform = :meth:`self.appian.visitor.visit_record_type(..)<appian_locust.visitor.Visitor.visit_record_type>`

_reports.py
===========
The _Reports class is no longer available. You may migrate any functionality using this class as follows:

.. list-table::
   :widths: 20 40 40
   :header-rows: 1

   * - Method in 1.x
     - Method in 2.x
     - Example Usage
   * - get_reports_interface
     - Not available anymore. Handled internally by the framework whenever it is necessary, so any calls to this can be removed without replacement.
     -
   * - get_reports_nav
     - Not available anymore. Handled internally by the framework whenever it is necessary, so any calls to this can be removed without replacement.
     -
   * - get_all
     - We can do the same operation by calling the “get_all_available_reports” in reports_info.py
     - reports_dict = :meth:`self.appian.reports_info.get_all_available_reports(..)<appian_locust.info.reports_info.ReportsInfo.get_all_available_reports>`
   * - get_report
     - We can do the same operation by calling the “get_report_info” in reports_info.py
     - report_info = :meth:`self.appian.reports_info.get_report_info(..)<appian_locust.info.reports_info.ReportsInfo.get_report_info>`
   * - visit_and_get_form
     - We can do the same operation by calling the “visit_report” in visitor.py
     - uiform = :meth:`self.appian.visitor.visit_report(..)<appian_locust.visitor.Visitor.visit_report>`
   * - visit
     - Not available. Instead call “visit_report” in visitor.py
     - uiform = :meth:`self.appian.visitor.visit_report(..)<appian_locust.visitor.Visitor.visit_report>`

_tasks.py
=========
The _Tasks class is no longer available. You may migrate any functionality using this class as follows:

.. list-table::
   :widths: 20 40 40
   :header-rows: 1

   * - Method in 1.x
     - Method in 2.x
     - Example Usage
   * - get_all
     - We can do the same operation by calling “get_all_available_tasks” method in tasks_info.py
     - tasks_dict = :meth:`self.appian.tasks_info.get_all_available_tasks(..)<appian_locust.info.tasks_info.TasksInfo.get_all_available_tasks>`
   * - get_task_pages
     - Not available. Handled internally by the framework whenever it is necessary, so any calls to this can be removed without replacement.
     -
   * - get_next_task_page_uri
     - Not available. Handled internally by the framework whenever it is necessary, so any calls to this can be removed without replacement.
     -
   * - visit_and_get_form
     - We can do the same operation by calling “visit_task” method in visitor.py
     - uiform =  :meth:`self.appian.visitor.visit_task(..)<appian_locust.visitor.Visitor.visit_task>`
   * - visit
     - Not available. Instead call “visit_task” in visitor.py
     - uiform =  :meth:`self.appian.visitor.visit_task(..)<appian_locust.visitor.Visitor.visit_task>`

_sites.py
===========
The _Sites class is no longer available. You may migrate any functionality using this class as follows:

.. list-table::
   :widths: 20 40 40
   :header-rows: 1

   * - Method in 1.x
     - Method in 2.x
     - Example Usage
   * - navigate_to_tab
     - Not available. Instead call “visit_site” in visitor.py
     - uiform =  :meth:`self.appian.visitor.visit_site(..)<appian_locust.visitor.Visitor.visit_site>`
   * - navigate_to_tab_and_record_if_applicable
     - Not available. Instead call “visit_site_recordlist_and_get_random_record_form” in visitor.py
     - record_instance_uiform =  :meth:`self.appian.visitor.visit_site_recordlist_and_get_random_record_form(..)<appian_locust.visitor.Visitor.visit_site_recordlist_and_get_random_record_form>`
   * - navigate_to_tab_and_record_get_form
     - We can do the same operation by calling “visit_site_recordlist_and_get_random_record_form” in visitor.py
     - record_instance_uiform =  :meth:`self.appian.visitor.visit_site_recordlist_and_get_random_record_form(..)<appian_locust.visitor.Visitor.visit_site_recordlist_and_get_random_record_form>`
   * - get_all
     - We can do the same operation by calling “get_all_available_sites” in sites_info.py
     - sites_dict = :meth:`self.appian.sites_info.get_all_available_sites()<appian_locust.info.sites_info.SitesInfo.get_all_available_sites>`
   * - get_site_data_by_site_name
     - We can do the same operation by calling “get_site_info” in sites_info.py
     - specific_site = :meth:`self.appian.sites_info.get_site_info(..)<appian_locust.info.sites_info.SitesInfo.get_site_info>`
   * - get_page_names_from_ui
     - Not available. Instead call “get_site_info” in sites_info.py
     - specific_site = :meth:`self.appian.sites_info.get_site_info(..)<appian_locust.info.sites_info.SitesInfo.get_site_info>`
   * - get_site_page
     - Not available. You can get page information from the Site object returned by “get_site_info” in sites_info.py
     - specific_site = :meth:`self.appian.sites_info.get_site_info(..)<appian_locust.info.sites_info.SitesInfo.get_site_info>`
   * - visit_and_get_form
     - We can do the same operation by calling “visit_site” in visitor.py
     - uiform =  :meth:`self.appian.visitor.visit_site(..)<appian_locust.visitor.Visitor.visit_site>`

_app_importer.py
================
The _app_importer module is no longer available. You may migrate any functionality using this module as follows:

.. list-table::
   :widths: 20 40 40
   :header-rows: 1

   * - Method in 1.x
     - Method in 2.x
     - Example Usage
   * - import_app
     - Available on DesignUiForm.py as “import_application”
     - | design_uiform = self.appian.visitor.visit_design()
       | :meth:`design_uiform.import_application(..)<appian_locust.uiform.design_uiform.DesignUiform.import_application>`

uiform.py
===========
The following methods in SailUiForm have removed or modified:

.. list-table::
   :widths: 20 40 40
   :header-rows: 1

   * - Method in 1.x
     - Method in 2.x
     - Example Usage
   * - get_record_header_form
     - Available on RecordInstanceUiForm.py as “get_header_view”
     - | record_form = self.appian.visitor.visit_record_instance(“record_type”, “record_name”)
       | record_header_form = :meth:`record_form.get_header_view()<appian_locust.uiform.record_instance_uiform.RecordInstanceUiform.get_header_view>`
   * - get_record_view_form
     - Available on RecordInstanceUiForm.py as “get_summary_view”
     - | record_form = self.appian.visitor.visit_record_instance(“record_type”, “record_name”)
       | record_header_form = :meth:`record_form.get_summary_view()<appian_locust.uiform.record_instance_uiform.RecordInstanceUiform.get_summary_view>`
   * - get_response
     - Not available. Instead use “get_latest_state”
     - :meth:`ui_form.get_latest_state()<appian_locust.uiform.SailUiForm.get_latest_state>`
   * - latest_state
     - Not available. Instead use “get_latest_state”
     - :meth:`ui_form.get_latest_state()<appian_locust.uiform.SailUiForm.get_latest_state>`
   * - get_latest_form
     - Not available. This method basically just returned “this”, so it was unnecessary.
     -
   * - click_record_link
     - This method now returns a new type, a RecordInstanceUiForm, so you must make sure to save the return value into a new variable
     - record_uiform: :class:`~appian_locust.uiform.record_instance_uiform.RecordInstanceUiform` = uiform.click_record_link(..)

_records_helper.py
==================
This class and all its methods are not accessible anymore.

_interactor.py
==============
This class and all its methods are not accessible anymore. There are corresponding methods in other new classes/existing classes.

Import Changes
==============
.. list-table::
   :widths: 20 40 40
   :header-rows: 1

   * - Class/Module
     - Import in V1
     - Import in V2
   * - helper
     - from appian_locust.helper import *
     - from appian_locust.utilities.helper import *
   * - Site
     - from appian_locust._sites import Site
     - from appian_locust.objects import Site
   * - Page
     - from appian_locust._sites import Page
     - from appian_locust.objects import Page
   * - PageType
     - from appian_locust._sites import PageType
     - from appian_locust.objects import PageType
   * - utls
     - from appian_locust.loadDriverUtils import utls
     - | from appian_locust.utilities import loadDriverUtils
       | utls = loadDriverUtils()
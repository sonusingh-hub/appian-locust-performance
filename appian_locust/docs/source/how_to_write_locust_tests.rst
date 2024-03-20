.. _how_to_write_locust_tests:

##########################
How to Write a Locust Test
##########################

The majority of the work involved in writing Appian Locust tests is around creating `Locust Tasks <https://docs.locust.io/en/stable/tasksets.html>`_. Each Task represents a workflow for a virtual Locust user to execute.
This section will go over how to get started writing tasks and introduce the two core Appian Locust concepts: the :class:`.Visitor` class and the :class:`.SailUiForm` class.

Sample Workflow
********************************************

For this workflow, we will use the **Employee Record Type** found in the Appian `documentation <https://docs.appian.com/suite/help/23.2/Records_Tutorial.html>`_.
We will implement a Locust Task that will create a new Employee record. The specific workflow will be as follows:

1. Navigate to the Employee Record List
2. Click the "New Employee" button
3. Fill in the  First Name, Last Name, Department, Title, and Phone Number fields
4. Click the "Create" button

Appian Navigation - Visitor
********************************************

The first step in most workflows is to navigate our user to an interface to interact with. All navigation in Appian Locust can be accomplished via the :class:`.Visitor`.
Any kind of Appian interface, including Sites, Records, Reports, Portals and others can be navigated to via the Visitor, and the Visitor will return a :class:`.SailUiForm` which
can be used to interact with that interface.

In our case, we want to navigate to a Record Type list. In Appian Locust, that would look like the following:

.. code-block:: python

    @task
    def create_new_employee(self):
        # Navigate to Employee Record List
        record_list_uiform = self.appian.visitor.visit_record_type(record_type="Employees")

UI Interactions - SailUiForm
********************************************

Now that we have navigated to the Employee Record List, we need to execute the workflow steps that will create the new Employee.
As briefly touched on above, all navigations done via the Visitor return a :class:`.SailUiForm` which is capable of performing interactions with a UI.
SailUiForm supports :meth:`filling in text fields <appian_locust.uiform.uiform.SailUiForm.fill_text_field>`,
:meth:`clicking buttons <appian_locust.uiform.uiform.SailUiForm.click_button>` and more.

In our specific case, because we navigated to a Record list, our visitor returned a subclass of the SailUiForm: the :class:`.RecordListUiForm`. Some types of
interfaces in Appian have a specific subclass that will support additional functionality catered to the kind of interface it represents. The RecordListUiForm will enable us to click
on the Record List Action which is unique to Record Lists via :meth:`click_record_list_action <appian_locust.uiform.record_list_uiform.RecordListUiForm.click_record_list_action>`, like so:

.. code-block:: python

    @task
    def create_new_employee(self):
        # Navigate to Employee Record List
        record_list_uiform = self.appian.visitor.visit_record_type(record_type="Employees")

        # Click on "New Employee" Record List Action
        record_list_uiform.click_record_list_action(label="New Employee")

As shown above, in many cases the only thing required to interact with a UI element is the label associated with that element.

At this point in the workflow, the dialog to create a new employee has been launched. Now we can use the various other interactions
supported by the base SailUiForm class which are available on all of its subclasses to fill out the new Employee's information:

.. code-block:: python

    @task
    def create_new_employee(self):
        # Navigate to Employee Record List
        record_list_uiform = self.appian.visitor.visit_record_type(record_type="Employees")

        # Click on "New Employee" Record List Action
        record_list_uiform.click_record_list_action(label="New Employee")

        # Fill in new Employee information
        record_list_uiform.fill_text_field(label="First Name", value="Sample")
        record_list_uiform.fill_text_field(label="Last Name", value="User")
        record_list_uiform.fill_text_field(label="Department", value="Engineering")
        record_list_uiform.fill_text_field(label="Title", value="Senior Software Engineer")
        record_list_uiform.fill_text_field(label="Phone Number", value="(703) 442-8844")

Now all we need to do is click the "Create" button, and our new Employee will be created!

.. code-block:: python

    @task
    def create_new_employee(self):
        # Navigate to Employee Record List
        record_list_uiform = self.appian.visitor.visit_record_type(record_type="Employees")

        # Click on "New Employee" Record List Action
        record_list_uiform.click_record_list_action(label="New Employee")

        # Fill in new Employee information
        record_list_uiform.fill_text_field(label="First Name", value="Sample")
        record_list_uiform.fill_text_field(label="Last Name", value="User")
        record_list_uiform.fill_text_field(label="Department", value="Engineering")
        record_list_uiform.fill_text_field(label="Title", value="Senior Software Engineer")
        record_list_uiform.fill_text_field(label="Phone Number", value="(703) 442-8844")

        # Create Employee!
        record_list_uiform.click_button(label="Create")

If you run a locust test with the task above, you should be able to check the Employee record list and see the "Sample User" employees that the virtual Locust user just made!
You can see a full version of a locust test including the task we just wrote `here <https://gitlab.com/appian-oss/appian-locust/-/blob/main/examples/example_create_employee_record.py>`_.
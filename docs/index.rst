.. Cucumber reports documentation master file, created by
   sphinx-quickstart on Sun Jan 29 23:24:02 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Cucumber reports's documentation!
============================================
This project aim to replace reporting tools for cucumber framework.

Short description
-----------------
This project is designed as standalone web application, which present data to users in two mains sections.
The data presented in application are obtained from provided data source, which implementation is out of scope of this project.


Reports
-------
First section of project provide reports from cucumber test executions.

Build execution report
----------------------
Provide reports for selected build run.

Feature report
--------------
Detailed report for selected feature run.
   - Background
   - Scenarios with their runs and data
   - Step results

Statistics
----------
Seconds section - provide statistics about executed cucumber tests.

Overview all build
------------------
First page you will see after you will select statistics.
Page list all existing projects last x of their executions.

Build development over time
---------------------------
For selected project provide statistics over its builds.


Build statistics
----------------
For selected build show detailed statistics.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules/models
   modules/converters
   modules/dao
   modules/view_models
   modules/views

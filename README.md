# Cucumber report GUI

Widely used testing framework Cucumber https://cucumber.io/ (for python there is no direct support so one of following
alternatives https://github.com/cucumber/cucumber/wiki/Python can be used instead) is today widely used to test mainly frontend
part of applications. However reporting tools provide only basic test outcome reporting like failed steps, failed features, duration time
 and nearly zero statistics about test outcomes see https://wiki.jenkins-ci.org/display/JENKINS/Cucumber+Reports+Plugin.

So this semestral work should serve as better solution as reporting tool via web application for testers and monitoring tool with more complex
view over tests and for business owner as tool to check quality and help plan test maintenance. More info in functionality section.

Final product is web application focused on detail test output reporting and some basic statistics about test outputs.
User (tester) should be able quickly find errors within tests with user friendly GUI.
User (business owner or some other project control role) is able to check stability of latest builds, number of tests,
tests failure rate development over time etc.

## Requirements
To successfully use this semestral work you will need data source with test outputs in specified data model. Right now is
supported only MongoDB. How to obtain data from runs does not belong to scope of this work.
Also technologies listed bellow will be required.

## Usage
1. Connect data source.
2. Deploy Django web application to your desired server with help of uncle google. There are so many types and each of them differ
so its meaningless to write deploy rules for each of them. But i will write down common outline.
  1. Copy this project to your server
  2. Create virtual env.
  3. Install required dependencies from by setup.py
  ```
  python setup.py install
  ```
  Note: requirement.txt contains requirements for Heroku so there are some additional
  dependencies, which are not need to run project locally.
  4. Specify data source and if needed perform database migrations by command executed in root directory of project
  ```
  python manage.py migrate cucumber_reports
  ```
  5. If needed change data source in cucumber_reporting/settings.py the is 
  variable DATABASES so change value to desired one.
  6. If you want to run project locally use:
  ```
  python manage.py runserver
  ```
  7. To manage local DB create super user with command
  ```
  python manage.py createsuperuser
  ```
  8. With created super user can be application managed at admin section accessible
  at URL <your_domain>/admin.
  9. Application prefix is <your_domain>/cucumber so this prefix will lead to index.html.
3. Open index.html and select reports or statistics section.
4. Inside statistics section you will see graph with test outputs development over time as two graphs. One with steps and second one with features per each build execution.
5. Inside reports section can user find latest test outputs and check their detail for more details.
Also browse results from older builds and more (depends on work involved).

## Examples
In project is included example_db.sqlite3 which contains some examples.
Install project dependencies:
```
python setup.py install
```
To run project locally with examples just type in root directory.

 ```
 python manage.py runserver
 ```

## Functionality

### Common
*  Page navigation
*  Link it together create some page site and design

### Reports
*  present all necessary information
   *  feature name
   *  description
   *  scenario definitions
   *  scenario runs with passed and failed steps
   *  replace placeholders with data
   *  source project
*  show/hide failed steps/runs

### Statistics
*  number of features passed/failed over time
*  number of features passed/failed in build run
*  number of passed/total count of steps in build run

This list is only general overview of the most important functionality. More details and necessary parts will reveal implementation so i will
update this list in future.

## Technologies
*  SQLite DB - there is not supported connector for MongoDB for last 4 years
*  Django
*  Pandas
*  Numpy
*  Pytest
*  ...


## Implementation troubles
* MongoDB connector for Django is no longer maintained so i have picked another DB - SQLite
* Sphinx can't import module with project so docs does not contain any doc strings from code.
  I have tried multiple configs/import variations but result was same.
* I have tried to deploy application on Heroku but there was problem with osgi configuration. 
  I am running out of time so only local host application is available right now.
  

  
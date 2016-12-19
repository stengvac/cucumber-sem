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
2. Deploy web application TODO create deploy instructions
3. Open index.html and select reports or statistics section.
4. Inside statistics section you will see graph with test outputs development over time and other graphs (TODO create some meaningful GUI)
5. Inside reports section can user find latest test outputs and check their detail for more details.
Also browse results from older builds and more (depends on work involved).

## Functionality

### Common
    * Page navigation
    * Link it together create some page site and design

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
*  number of passed/failed/skipped/pending steps

This list is only general overview of the most important functionality. More details and necessary parts will reveal implementation so i will
update this list in future.

## Technologies
*  MongoDB - contains results from Cucumber tests
*  Django
*  Pandas
*  Numpy
*  Pytest
*  ...

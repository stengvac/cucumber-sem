# Cucumber report GUI


Widely used testing framework Cucumber https://cucumber.io/ (for python there is no direct support so one of following
alternatives https://github.com/cucumber/cucumber/wiki/Python can be used instead) is today widely used to test mainly frontend
part of applications. However reporting tools provide only basic test outcome reporting like failed steps, failed features, duration time
 and nearly zero statistics about test outcomes see https://wiki.jenkins-ci.org/display/JENKINS/Cucumber+Reports+Plugin.

So this semestral work should serve as better solution as reporting tool for testers and monitoring tool with more complex
view over tests. More info in functionality section.
 and for business owner as tool to check quality and help plan test maintenance.

## Functionality

### Common
    * Page navigation
    * Link it together create some page site and design

### Reports
    * present all necessary information
        * feature name
        * description
        * scenario definitions
        * scenario runs with passed and failed steps
        * replace placeholders with data
        * source project
    * show/hide failed steps/runs
### Statistics
    * number of features passed/failed over time
    * number of features passed/failed in build run
    * number of passed/failed/skipped/pending steps

This list is only general overview of the most important functionality. More details and necessary parts will reveal implementation so i will
update this list in future.

## Technologies
    * MongoDB - contains results from Cucumber tests
    * Django
    * Pandas
    * Numpy
    * Pytest
    * ...

from django.db import models

"""Possible step run results"""
StepStatus = (
    ('p', 'PASSED'),
    ('f', 'FAILED'),
    ('m', 'MISSING'),
    ('s', 'SKIPPED'),
    ('e', 'PENDING')
)

""" Possible scenario definition types:

    SCENARIO_OUTLINE - scenario definition type with multiple runs
    SCENARIO - scenario with one run
    BACKGROUND - feature background with data/functionality for whole feature
"""
ScenarioType = (
    ('o', 'SCENARIO_OUTLINE'),
    ('s', 'SCENARIO'),
    ('b', 'BACKGROUND')
)


class BuildRun(models.Model):
    """
    Representation of one project build run.

    Build run with build_name and build_number was executed at date build_at.
    """
    build_number = models.IntegerField(null=False)
    build_name = models.CharField(max_length=200)
    build_at = models.DateTimeField()

    def passed(self):
        return passed(self.features.iterator())

    def __str__(self):
        return '{} {}'.format(self.build_name, self.build_number)

    class Meta:
        ordering = ['build_name', 'build_number']
        managed = True


class Feature(models.Model):
    """
    Representation of feature file executed in build run.

    name - name of feature file
    description - description inside feature file
    glue - path to files with step implementations which are needed to execute step definitions in feature
    build_run - which executed this feature
    """
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    glue = models.CharField(max_length=200)
    build_run = models.ForeignKey(BuildRun, related_name='features')

    def passed(self):
        """Return true when there are no failed scenario runs."""
        return passed(self.scenario_definitions.iterator())

    def __str__(self):
        """String representation - feature name"""
        return '{}'.format(self.name)

    class Meta:
        managed = True


class ScenarioDefinition(models.Model):
    """
    Representation of scenario definition inside feature

    name - scenario def name
    description - description of definition
    type - of scenario see ScenarioType variable doc
    feature - feature containing this definition
    """
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=1, choices=ScenarioType)
    feature = models.ForeignKey(Feature, related_name='scenario_definitions')
    description = models.CharField(max_length=300, null=True, blank=True)

    def passed(self):
        """Return True when there are no failures in definition runs."""
        return passed(self.scenario_runs.iterator())

    def __str__(self):
        """Scenario definition string representation - name and type"""
        return '{} {}'.format(self.name, self.type)

    class Meta:
        managed = True


class ScenarioRun(models.Model):
    """
    Execution results of scenario definition.

    scenario_definition - contains definitions of steps which were executed during this run
    """
    scenario_definition = models.ForeignKey(ScenarioDefinition, related_name='scenario_runs')

    def passed(self):
        """Return True when all executed steps have status PASSED"""
        return passed(self.step_runs.iterator())

    def __str__(self):
        """Scenario definition string representation - name and type"""
        return '{} -  {} - {}'.format(self.scenario_definition.feature.name,
                                      self.scenario_definition.name, self.scenario_definition.type)

    class Meta:
        managed = True


class StepDefinition(models.Model):
    """
    Step definition representation - steps inside scenario definitions which are executed during tests.

    name - step name
    keyword - keyword before step definition - specify purpose of step. Right now possible keywords are
        @Given - step setup data
        @And - step in scenario - perform some functionality
        @When - performed some functionality - with excepted result
        @Then - check if result is correct
    scenario_definition - which holds this definition
    """
    name = models.CharField(max_length=200)
    keyword = models.CharField(max_length=20)
    scenario_definition = models.ForeignKey(ScenarioDefinition, related_name='step_definitions')

    def __str__(self):
        """String representation - keyword and name"""
        return '{} {}'.format(self.keyword, self.name)

    class Meta:
        managed = True


class StepRun(models.Model):
    """
    Run of step definition in scenario run.

    duration - step execution duration
    status - the result of step execution. see StepStatus for more info.
    error_msg - first failed step in scenario run contains error message
    scenario_run - scenario execution which hold this step execution
    """
    duration = models.BigIntegerField()
    status = models.CharField(max_length=1, choices=StepStatus)
    error_msg = models.CharField(max_length=200, null=True, blank=True)
    scenario_run = models.ForeignKey(ScenarioRun, related_name='step_runs')

    def passed(self):
        """Return True when status is PASSED"""
        return self.status == StepStatus[0][0]

    def __str__(self):
        """String representation status and duration"""
        return '{}-{}-{}'.format(self.scenario_run.scenario_definition.name, self.status, self.duration)

    class Meta:
        managed = True


def passed(runs):
    """Return True when there is no failure within collection elements."""
    for run in runs:
        if not run.passed():
            return False
    return True

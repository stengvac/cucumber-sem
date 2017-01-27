from django.db import models


StepStatus = (
    ('p', 'PASSED'),
    ('f', 'FAILED'),
    ('m', 'MISSING'),
    ('s', 'SKIPPED'),
    ('e', 'PENDING')
)

ScenarioType = (
    ('o', 'SCENARIO OUTLINE'),
    ('s', 'SCENARIO'),
    ('b', 'BACKGROUND')
)


class BuildRun(models.Model):
    build_number = models.IntegerField(null=False)
    build_name = models.CharField(max_length=200)
    build_at = models.DateTimeField()

    def passed(self):
        return passed(self.features.iterator())

    def __str__(self):
        return '{} {}'.format(self.build_name, self.build_number)


class Feature(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    glue = models.CharField(max_length=200)
    build_run = models.ForeignKey(BuildRun, related_name='features')

    def passed(self):
        return passed(self.scenario_definitions.iterator())

    def __str__(self):
        return '{}'.format(self.name)


class ScenarioDefinition(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=1, choices=ScenarioType)
    feature = models.ForeignKey(Feature, related_name='scenario_definitions')
    description = models.CharField(max_length=300, null=True, blank=True)

    def passed(self):
        return passed(self.scenario_runs.iterator())

    def __str__(self):
        return '{} {}'.format(self.name, self.type)


class ScenarioRun(models.Model):
    scenario_definition = models.ForeignKey(ScenarioDefinition, related_name='scenario_runs')

    def passed(self):
        return passed(self.step_runs.iterator())

    def __str__(self):
        return '{}'.format(self.name)


class StepDefinition(models.Model):
    name = models.CharField(max_length=200)
    keyword = models.CharField(max_length=20)
    scenario_definition = models.ForeignKey(ScenarioDefinition, related_name='step_definitions')

    def __str__(self):
        return '{} {}'.format(self.keyword, self.name)


class StepRun(models.Model):
    duration = models.BigIntegerField()
    status = models.CharField(max_length=1, choices=StepStatus)
    error_msg = models.CharField(max_length=200, null=True, blank=True)
    scenario_run = models.ForeignKey(ScenarioRun, related_name='step_runs')

    def passed(self):
        return self.status == StepStatus[0][1]

    def __str__(self):
        return '{}-{}'.format(self.status, self.duration)


def passed(runs):
    """Return true when all objects in collection passed"""
    for run in runs:
        if not run.passed():
            return False
    return True

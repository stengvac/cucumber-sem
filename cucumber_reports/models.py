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


class StepRun(models.Model):
    duration = models.BigIntegerField()
    status = models.CharField(max_length=1, choices=StepStatus)
    error_msg = models.CharField(max_length=200)


class StepDefinition(models.Model):
    name = models.CharField(max_length=200)
    keyword = models.CharField(max_length=20)


class ScenarioRun(models.Model):
    name = models.CharField(max_length=200)
    step_runs = models.ForeignKey(StepRun)


class ScenarioDefinition(models.Model):
    name = models.CharField(max_length=200)
    scenario_runs = models.ForeignKey(ScenarioRun)
    step_definitions = models.ForeignKey(StepDefinition)
    type = models.CharField(max_length=1, choices=ScenarioType)


class Feature(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    scenario_definitions = models.ForeignKey(ScenarioDefinition)








class BuildRun(models.Model):
    build_number = models.IntegerField(null=False)
    build_name = models.CharField(max_length=200)
    features = models.ForeignKey(Feature)


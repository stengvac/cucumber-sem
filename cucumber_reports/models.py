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
    error_msg = models.CharField(max_length=200, null=True, blank=True)

    def passed(self):
        return self.status == StepStatus[0][1]

    class Meta:
        db_table = 'step_run'


class StepDefinition(models.Model):
    name = models.CharField(max_length=200)
    keyword = models.CharField(max_length=20)

    class Meta:
        db_table = 'step_def'


class ScenarioRun(models.Model):
    name = models.CharField(max_length=200)
    step_runs = models.ForeignKey(StepRun)

    def passed(self):
        return passed(self.step_runs)

    class Meta:
        db_table = 'scenario_run'


class ScenarioDefinition(models.Model):
    name = models.CharField(max_length=200)
    scenario_runs = models.ForeignKey(ScenarioRun)
    step_definitions = models.ForeignKey(StepDefinition)
    type = models.CharField(max_length=1, choices=ScenarioType)

    def passed(self):
        return passed(self.scenario_runs)

    class Meta:
        db_table = 'scenario_def'


class Feature(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    scenario_definitions = models.ForeignKey(ScenarioDefinition)

    def passed(self):
        return passed(self.scenario_definitions)

    class Meta:
        db_table = 'feature'


class BuildRun(models.Model):
    build_number = models.IntegerField(null=False)
    build_name = models.CharField(max_length=200)
    build_at = models.DateTimeField()
    features = models.ForeignKey(Feature, blank=True, null=True)

    def passed(self):
        return passed(self.features)

    class Meta:
        db_table = 'build_run'


def passed(runs):
    """Return true when all objects in collection passed"""
    for run in runs:
        if not run.passed():
            return False
    return True

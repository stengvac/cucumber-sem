from enum import Enum


class Statement:
    """Statement - super class of nearly all feature objects"""
    def __init__(self, name, description):
        self.name = name
        self.description = description


class BuildRunReport:
    """One build run can contain multiple features."""
    def __init__(self, metadata, passed, features):
        self.metadata = metadata
        self.passed = passed
        self.features = features


class FeatureMetadata:
    def __init__(self, name, passed):
        self.name = name
        self.passed = passed


class BuildRunMetadata:
    """Common information about build run"""
    def __init__(self, name, number, build_at):
        self.name = name
        self.number = number
        self.build_at = build_at


class FeatureReport(Statement):
    """Feature contains multiple test scenarios."""
    def __init__(self, name, description, definitions, background, metadata):
        super().__init__(name, description)
        self.build_metadata = metadata
        self.scenario_definitions = definitions
        self.background = background

    def passed(self):
        """Return true when all scenario definitions with all their runs finished without failures"""
        return passed(self.scenario_definitions)


class ScenarioDefinitionReport(Statement):
    """One scenario definition representation. Can be executed multiple times if its type is OUTLINE."""
    def __init__(self, name, description, runs, type, step_definitions):
        super().__init__(name, description)
        self.runs = runs
        self.type = type
        self.step_definitions = step_definitions

    def scenario_outline(self):
        """Return true when instance is scenario outline."""
        return self.type == ScenarioType.SCENARIO_OUTLINE

    def passed(self):
        """Return true when all runs passed without failure"""
        return passed(self.runs)


class ScenarioRun:
    """Represent one scenario run."""
    def __init__(self, steps, bg_steps):
        self.step_runs = steps
        self.bg_steps = bg_steps

    def passed(self):
        return passed(self.step_runs) and passed(self.bg_steps)


class StepDefinition(Statement):
    """Step definition inside scenario definition"""
    def __init__(self, name, description, keyword):
        super().__init__(name, description)
        self.keyword = keyword


class StepRun:
    """Represent step run of associated step definition"""
    def __init__(self, status, duration, error_msg):
        self.duration = duration
        self.error_msg = error_msg
        self.status = status

    def passed(self):
        """Step run passed when its status eq PASSED otherwise run failed"""
        return StepStatus.PASSED == self.status


class StepStatus(Enum):
    """Step status - represent status result."""
    PASSED = 'p',
    FAILED = 'f',
    SKIPPED = 's',
    PENDING = 'e',
    MISSING = 's'

    @classmethod
    def from_string(cls, value):
        return getattr(cls, value, None)


class ScenarioType(Enum):
    """Type of scenario."""
    SCENARIO = 'SCENARIO',
    SCENARIO_OUTLINE = 'SCENARIO_OUTLINE',
    BACKGROUND = 'BACKGROUND'

    @classmethod
    def from_string(cls, value):
        return getattr(cls, value, None)


class BuildOverTimeStatistics:
    def __init__(self, step_runs, features_cnt, features_passed, steps_passed, meta):
        self.features_cnt = features_cnt
        self.step_runs = step_runs
        self.features_passed = features_passed
        self.steps_passed = steps_passed
        self.metadata = meta


class OverViewReport:
    def __init__(self, name):
        self.name = name
        self.runs = []


class BuildRunReport:
    def __init__(self, number, build_at, passed):
        self.number = number
        self.build_at = build_at
        self.passed = passed


class FeatureStatistic:
    def __init__(self, passed, step_cnt, step_run_cnt, step_passed_cnt):
        self.passed = passed
        self.step_cnt = step_cnt
        self.step_run_cnt = step_run_cnt
        self.step_passed_cnt = step_passed_cnt
        self.step_failed_cnt = step_run_cnt - step_passed_cnt
        self.scenario_def_cnt = None


def passed(runs):
    """Return true when all objects in collection passed"""
    for run in runs:
        if not run.passed():
            return False
    return True

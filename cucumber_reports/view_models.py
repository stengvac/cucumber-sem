from enum import Enum


class Statement:
    """
    Statement - super class for nearly all feature objects

    name - name of statement.
    description - more detailed text about statement
    """
    def __init__(self, name, description):
        """Instance initialization"""
        self.name = name
        self.description = description


class BuildRunReport:
    """
    View model for: report of build run. Contains build run metadata like build_name, build_number and results of executed features
    in this build run.

    metadata - build run metadata
    features - reports of executed feature files in this build run
    """
    def __init__(self, metadata, features):
        """Instance initialization"""
        self.metadata = metadata
        self.features = features


class BuildRunMetadata:
    """
    View model for: build run metadata.

    name - build run name
    number - build run sequence number
    build_at - data of build execution
    passed - true when whole build run does not contain any failed feature runs
    """
    def __init__(self, name, number, build_at, passed):
        """Instance initialization"""
        self.name = name
        self.number = number
        self.build_at = build_at
        self.passed = passed


class FeatureReport(Statement):
    """
    View model for: Feature report. Feature report mirror feature execution in build run.

    build_metadata
    scenario_definitions - Definitions of all scenarios present in feature file
    background - Background definition (not necessary present)
    """
    def __init__(self, name, description, definitions, background, build_metadata):
        """Instance initialization"""
        super().__init__(name, description)
        self.build_metadata = build_metadata
        self.scenario_definitions = definitions
        self.background = background

    def passed(self):
        """Return true when all scenario definitions with all their runs finished without failures"""
        return passed(self.scenario_definitions)


class ScenarioDefinitionReport(Statement):
    """
    View model for: Scenario definition report. Contains steps definitions and its executions in scenario runs
    (some scenarios can be executed multiple times with different data sets).

    runs - scenario definition executions
    type - of scenario definition
    """
    def __init__(self, name, description, runs, type):
        """Instance initialization"""
        super().__init__(name, description)
        self.runs = runs
        self.type = type

    def scenario_outline(self):
        """Return true when instance is scenario outline."""
        return self.type == ScenarioType.SCENARIO_OUTLINE

    def passed(self):
        """Return true when all runs passed without failure"""
        return passed(self.runs)


class ScenarioRun:
    """
    View model for: Scenario run report. Contains scenario and background step runs - results of step esecution.

    step_runs - scenario step runs
    bg_steps - background step runs
    """
    def __init__(self, steps, bg_steps):
        """Instance initialization"""
        self.step_runs = steps
        self.bg_steps = bg_steps

    def passed(self):
        """Return True when all scenario and background step runs passed"""
        return passed(self.step_runs) and passed(self.bg_steps)


class StepDefinition(Statement):
    """Step definition inside scenario definition"""
    def __init__(self, name, description, keyword):
        super().__init__(name, description)
        self.keyword = keyword


class StepRun:
    """Represent step run of associated step definition"""
    def __init__(self, definition, status, duration, error_msg):
        self.step_def = definition
        self.duration = duration
        self.error_msg = error_msg
        self.status = status

    def passed(self):
        """Step run passed when its status eq PASSED otherwise run failed"""
        return StepStatus.PASSED == self.status


class StepStatus(Enum):
    """Step status - represent step execution result."""
    PASSED = 'p',
    FAILED = 'f',
    SKIPPED = 's',
    PENDING = 'e',
    MISSING = 's'

    @classmethod
    def from_string(cls, value):
        """Return enum value for string value. Return None if enum not found or ars is None."""
        return getattr(cls, value, None)


class ScenarioType(Enum):
    """Type of scenario."""
    SCENARIO = 'SCENARIO',
    SCENARIO_OUTLINE = 'SCENARIO_OUTLINE',
    BACKGROUND = 'BACKGROUND'

    @classmethod
    def from_string(cls, value):
        """Return enum value for string value. Return None if enum not found or ars is None."""
        return getattr(cls, value, None)


class BuildOverTimeDevelopmentStatistics:
    """
    View model for: Build runs over time development.

    feature_count - number of executed feature files in build run
    step_runs - number of executed step runs in build run
    features_passed - count of passed features ie there is no failure in their execution
    steps_passed - number of passed steps from all step executions
    metadata - build run metadata so we can tell source of data
    """
    def __init__(self, step_runs, features_cnt, features_passed, steps_passed, meta):
        """Instance initialization"""
        self.features_cnt = features_cnt
        self.step_runs = step_runs
        self.features_passed = features_passed
        self.steps_passed = steps_passed
        self.metadata = meta


class OverViewReport:
    """
    View model for: Builds overview report.

    name - project name
    runs - last n build runs
    """
    def __init__(self, name):
        """Instance initialization"""
        self.name = name
        self.runs = []


class BuildRunStatistics:
    """
    View model for: Build run statistics.

    metadata - build run metadata
    feature_statistics = statistics about features executed during build
    """
    def __init__(self, metadata, features):
        """Instance initialization"""
        self.metadata = metadata
        self.feature_statistics = features


class FeatureStatistic:
    """
    View model for: Feature statistics.

    name - feature name
    step_cnt - count of steps definitions inside feature also include background steps
    step_run_cnt - number of step executions
    step_passed_cnt - count of passed steps
    step_failed_cnt - total - passed steps

    """
    def __init__(self, name, step_cnt, step_run_cnt, step_passed_cnt):
        self.name = name
        self.step_cnt = step_cnt
        self.step_run_cnt = step_run_cnt
        self.step_passed_cnt = step_passed_cnt
        self.step_failed_cnt = step_run_cnt - step_passed_cnt
        self.scenario_def_cnt = None

    def passed(self):
        """Feature passed if number of steps runs eq number of passed steps"""
        return self.step_run_cnt == self.step_passed_cnt


def passed(runs):
    """Return true when all objects in collection passed"""
    for run in runs:
        if not run.passed():
            return False
    return True

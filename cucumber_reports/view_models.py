from enum import Enum


class Statement:
    """
    Statement - super class for nearly all feature objects
    """
    def __init__(self, name, description):
        """

        :param name: name of statement
        :param description: more detailed text about statement
        """
        self.name = name
        self.description = description


class BuildRunReport:
    """
    View model for: report of build run. Contains build run metadata like build_name, build_number and results of executed features
    in this build run.
    """
    def __init__(self, metadata, features):
        """

        :param metadata: build run metadata
        :param features: reports of executed feature files in this build run
        """
        self.metadata = metadata
        self.features = features
        self.previous = metadata.number - 1
        self.next = metadata.number + 1


class FeatureMetadata(Statement):
    """
    Metadata about feature
    """

    def __init__(self, name, description, passed):
        """
        Instance initialization
        :param name: feature name
        :param description: feature description
        :param passed: feature passed or not
        """
        super().__init__(name, description)
        self.passed = passed


class BuildRunMetadata:
    """
    View model for: build run metadata.
    """
    def __init__(self, name, number, build_at, passed):
        """

        :param name: build run name
        :param number: build run sequence number
        :param build_at: data of build execution
        :param passed: true when whole build run does not contain any failed feature runs
        """
        self.name = name
        self.number = number
        self.build_at = build_at
        self.passed = passed


class FeatureReport(Statement):
    """
    View model for: Feature report. Feature report mirror feature execution in build run.
    """
    def __init__(self, name, description, definitions, background, build_metadata, glue):
        """

        :param name: feature name
        :param description: feature description
        :param definitions: scenario_definitions - Definitions of all scenarios present in feature file
        :param background: Background definition (not necessary present)
        :param build_metadata:
        """
        super().__init__(name, description)
        self.build_metadata = build_metadata
        self.scenario_definitions = definitions
        self.background = background
        self.glue = glue

    def passed(self):
        """Return true when all scenario definitions with all their runs finished without failures"""
        return passed(self.scenario_definitions)


class ScenarioDefinitionReport(Statement):
    """
    View model for: Scenario definition report. Contains steps definitions and its executions in scenario runs
    (some scenarios can be executed multiple times with different data sets).
    """
    def __init__(self, name, description, runs, type):
        """

        :param name: scenario name
        :param description: scenario description
        :param runs: scenario definition executions
        :param type: of scenario definition
        """
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
    """
    def __init__(self, steps, bg_steps):
        """

        :param steps: scenario step runs
        :param bg_steps: background step runs
        """
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
        """

        :param definition: associated step definition
        :param status: step execution result
        :param duration: duration of step execution
        :param error_msg: msg what went wrong
        """
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
    MISSING = 'm',
    SKIPPED = 's',
    PENDING = 'e',

    @classmethod
    def from_string(cls, value):
        """Return enum value for string value. Return None if enum not found or ars is None."""
        print(value)
        for status in StepStatus:
            if status.value[0] == value:
                return status
        return None


class ScenarioType(Enum):
    """Type of scenario."""
    SCENARIO_OUTLINE = 'o',
    SCENARIO = 's',
    BACKGROUND = 'b'

    @classmethod
    def from_string(cls, value):
        """Return enum value for string value. Return None if enum not found or ars is None."""
        for type in ScenarioType:
            if type.value[0] == value:
                return type
        return None


class BuildOverTimeDevelopmentStatistics:
    """
    View model for: Build runs over time development.
    """
    def __init__(self, step_runs, features_cnt, features_passed, steps_passed, meta):
        """

        :param step_runs:  number of executed step runs in build run
        :param features_cnt: number of executed feature files in build run
        :param features_passed: count of passed features ie there is no failure in their execution
        :param steps_passed: number of passed steps from all step executions
        :param meta: build run metadata so we can tell source of data
        """
        self.features_cnt = features_cnt
        self.step_runs = step_runs
        self.features_passed = features_passed
        self.steps_passed = steps_passed
        self.metadata = meta


class OverViewReport:
    """
    View model for: Builds overview report.

    runs - last n build runs
    """
    def __init__(self, name):
        """

        :param name: project name
        """
        self.name = name
        self.runs = []


class BuildRunStatistics:
    """
    View model for: Build run statistics.
    """
    def __init__(self, metadata, features):
        """

        :param metadata: build run metadata
        :param features: statistics about features executed during build
        """
        self.metadata = metadata
        self.feature_statistics = features


class FeatureStatistic:
    """
    View model for: Feature statistics.
    """
    def __init__(self, name, step_cnt, step_run_cnt, step_passed_cnt, scenario_definitions, scenario_runs):
        """

        :param name: feature name
        :param step_cnt: count of steps definitions inside feature also include background steps
        :param step_run_cnt: number of step executions
        :param step_passed_cnt: count of passed steps
        """
        self.name = name
        self.step_cnt = step_cnt
        self.step_run_cnt = step_run_cnt
        self.step_passed_cnt = step_passed_cnt
        self.step_failed_cnt = step_run_cnt - step_passed_cnt
        self.scenario_def_cnt = scenario_definitions
        self.scenario_run_cnt = scenario_runs

    def passed(self):
        """Feature passed if number of steps runs eq number of passed steps"""
        return self.step_run_cnt == self.step_passed_cnt


def passed(runs):
    """Return true when all objects in collection passed"""
    for run in runs:
        if not run.passed():
            return False
    return True

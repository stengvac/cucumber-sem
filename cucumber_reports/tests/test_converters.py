from cucumber_reports import converters
from cucumber_reports import models, view_models
from datetime import date
import pytest

BUILD_AT = date(2017, 1, 29)
BUILD_NAME = 'b_name'
BUILD_NUMBER = 12
FEATURE_NAME = 'f_name'
FEATURE_DESC = 'f_desc'
STEP_NAME = 's_name'
STEP_KEYWORD = 's_key'
STEP_DURATION = 4000
STEP_RESULT_PASSED = view_models.StepStatus.PASSED.value[0]
STEP_RESULT_FAILED = view_models.StepStatus.FAILED.value[0]
TYPE_SCENARIO = view_models.ScenarioType.SCENARIO.value[0]
ERROR_MSG = 'msg'
SCENARIO_NAME = 's_name'
SCENARIO_DESC = 's_desc'


@pytest.mark.django_db
def test_convert_build_metadata():
    result = converters.convert_build_metadata(create_build_run())

    assert result
    assert BUILD_AT == result.build_at
    assert BUILD_NUMBER == result.number
    assert BUILD_NAME == result.name


@pytest.mark.django_db
def test_convert_build_run():
    build_run = create_build_run()
    create_feature(build_run)

    result = converters.convert_build_run(build_run)

    assert result
    assert 1 == len(result.features)
    assert FEATURE_NAME == result.features[0].name
    assert FEATURE_DESC == result.features[0].description
    assert BUILD_NAME == result.metadata.name


def test_convert_feature_metadata():
    feature = models.Feature(name=FEATURE_NAME, description=FEATURE_DESC)
    result = converters.convert_feature_metadata(feature)

    assert result
    assert FEATURE_NAME == result.name
    assert FEATURE_DESC == result.description


def test_convert_step_definition():
    result = converters.convert_step_definition(models.StepDefinition(name=STEP_NAME, keyword=STEP_KEYWORD))

    assert result
    assert STEP_NAME == result.name
    assert STEP_KEYWORD == result.keyword
    assert not result.description


def test_convert_step_runs():
    run = models.StepRun()
    run.duration = STEP_DURATION
    run.error_msg = ERROR_MSG
    run.status = STEP_RESULT_PASSED

    result = converters.convert_step_runs([models.StepDefinition(name=STEP_NAME, keyword=STEP_KEYWORD)], [run])

    assert result
    assert 1 == len(result)
    result = result[0]
    assert view_models.StepStatus.PASSED == result.status
    assert STEP_DURATION == result.duration
    assert ERROR_MSG == result.error_msg
    assert result.step_def
    assert STEP_NAME == result.step_def.name


def test_find_background():
    scenario_outline = models.ScenarioDefinition(type=view_models.ScenarioType.SCENARIO_OUTLINE.value[0])
    scenario = models.ScenarioDefinition(type=TYPE_SCENARIO)
    background = models.ScenarioDefinition(type=view_models.ScenarioType.BACKGROUND.value[0])

    result = converters._find_background([scenario_outline, scenario, background])

    assert result
    assert background == result


@pytest.mark.django_db
def test_convert_scenario_definition():

    scenario = create_scenario_definition(create_feature(create_build_run()), TYPE_SCENARIO)
    create_scenario_run(scenario)

    result = converters.convert_scenario_definition(scenario)

    assert result
    assert SCENARIO_DESC == result.description
    assert SCENARIO_NAME == result.name
    assert view_models.ScenarioType.SCENARIO == result.type
    assert 1 == len(result.runs)


@pytest.mark.django_db
def test_convert_build_run_statistics():
    build_run = create_build_run()
    feature = create_feature(build_run)
    scenario_def = create_scenario_definition(feature, TYPE_SCENARIO)
    scenario_run = create_scenario_run(scenario_def)
    create_step_run(scenario_run, STEP_RESULT_FAILED)
    create_step_run(scenario_run, STEP_RESULT_PASSED)
    create_step_definition(scenario_def)

    result = converters.convert_build_run_statistics(build_run)

    assert result
    assert BUILD_NAME == result.metadata.name
    assert 1 == len(result.feature_statistics)
    feature_stats = result.feature_statistics[0]
    assert FEATURE_NAME == feature_stats.name
    assert 1 == feature_stats.step_cnt
    assert 2 == feature_stats.step_run_cnt
    assert 1 == feature_stats.step_passed_cnt
    assert 1 == feature_stats.step_failed_cnt


@pytest.mark.django_db
def test_convert_development_over_time():
    build_run = create_build_run()
    feature = create_feature(build_run)
    scenario_def = create_scenario_definition(feature, TYPE_SCENARIO)
    scenario_run = create_scenario_run(scenario_def)
    create_step_run(scenario_run, STEP_RESULT_PASSED)
    create_step_run(scenario_run, STEP_RESULT_PASSED)
    create_step_definition(scenario_def)

    build_run2 = create_build_run()
    feature = create_feature(build_run2)
    scenario_def = create_scenario_definition(feature, TYPE_SCENARIO)
    scenario_run = create_scenario_run(scenario_def)
    create_step_run(scenario_run, STEP_RESULT_FAILED)
    create_step_definition(scenario_def)

    result = converters.convert_development_over_time([build_run, build_run2])

    assert 2 == len(result)
    stat1 = result[0]
    assert 1 == stat1.features_cnt
    assert 2 == stat1.step_runs
    assert 1 == stat1.features_passed
    assert BUILD_NAME == stat1.metadata.name
    assert stat1.metadata.passed
    stat1 = result[1]
    assert 1 == stat1.features_cnt
    assert 1 == stat1.step_runs
    assert 0 == stat1.features_passed
    assert BUILD_NAME == stat1.metadata.name
    assert not stat1.metadata.passed


def create_build_run():
    return models.BuildRun.objects.create(build_name=BUILD_NAME, build_at=BUILD_AT, build_number=BUILD_NUMBER)


def create_feature(build_run):
    return models.Feature.objects.create(build_run=build_run, name=FEATURE_NAME, description=FEATURE_DESC)


def create_scenario_definition(feature, type):
    return models.ScenarioDefinition.objects.create(type=type, feature=feature,
                                                    description=SCENARIO_DESC, name=SCENARIO_NAME)


def create_step_definition(scenario_definition):
    return models.StepDefinition.objects.create(name=STEP_NAME, keyword=STEP_KEYWORD,
                                                scenario_definition=scenario_definition)


def create_scenario_run(scenario_definition):
    return models.ScenarioRun.objects.create(scenario_definition=scenario_definition)


def create_step_run(scenario_run, status):
    return models.StepRun.objects.create(duration=STEP_DURATION, status=status,
                                         error_msg=ERROR_MSG, scenario_run=scenario_run)

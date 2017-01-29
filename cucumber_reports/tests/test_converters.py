from cucumber_reports import converters
from cucumber_reports import models, view_models
from datetime import datetime, date
import django
import pytest

BUILD_AT = date(2017, 1, 29)
BUILD_NAME = 'b_name'
BUILD_NUMBER = '12'
FEATURE_NAME = 'f_name'
FEATURE_DESC = 'f_desc'
STEP_NAME = 's_name'
STEP_KEYWORD = 's_key'
STEP_DURATION = 4000
STEP_RESULT = models.StepStatus[0][1]
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
    feature = models.Feature.objects.create(name=FEATURE_NAME, description=FEATURE_DESC, build_run=build_run)
    build_run.features = [feature]

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


def test_convert_feature_report():
    pass


def test_convert_step_definition():
    result = converters.convert_step_definition(create_step_definition())

    assert result
    assert STEP_NAME == result.name
    assert STEP_KEYWORD == result.keyword
    assert not result.description


def test_convert_step_runs():
    run = models.StepRun()
    run.duration = STEP_DURATION
    run.error_msg = ERROR_MSG
    run.status = STEP_RESULT

    result = converters.convert_step_runs([create_step_definition()], [run])

    assert result
    assert 1 == len(result)
    result = result[0]
    assert view_models.StepStatus.PASSED == result.status
    assert STEP_DURATION == result.duration
    assert ERROR_MSG == result.error_msg
    assert result.step_def
    assert STEP_NAME == result.step_def.name


def test_find_background():
    scenario_outline = models.ScenarioDefinition(type=models.ScenarioType[0][1])
    scenario = models.ScenarioDefinition(type=models.ScenarioType[1][1])
    background = models.ScenarioDefinition(type=models.ScenarioType[2][1])

    result = converters._find_background([scenario_outline, scenario, background])

    assert result
    assert background == result


@pytest.mark.django_db
def test_convert_scenario_definition():

    scenario = models.ScenarioDefinition.objects.create(type=models.ScenarioType[1][1], name=SCENARIO_NAME,
                                                        description=SCENARIO_DESC, feature=create_feature())
    models.ScenarioRun.objects.create(scenario_definition=scenario)

    result = converters.convert_scenario_definition(scenario)

    assert result
    assert SCENARIO_DESC == result.description
    assert SCENARIO_NAME == result.name
    assert view_models.ScenarioType.SCENARIO == result.type
    assert 1 == len(result.runs)


def create_build_run():
    return models.BuildRun.objects.create(build_name=BUILD_NAME, build_at=BUILD_AT, build_number=BUILD_NUMBER)


def create_step_definition():
    step = models.StepDefinition()
    step.name = STEP_NAME
    step.keyword = STEP_KEYWORD

    return step


def test_convert_scenario_runs():
    pass


def create_scenario_run():
    return models.ScenarioRun()


def create_feature():
    return models.Feature.objects.create(build_run=create_build_run())
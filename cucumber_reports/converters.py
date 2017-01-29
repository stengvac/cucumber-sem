from . import view_models
from . import models


def convert_build_run(build_run):
    """Convert dao build run to view build run"""
    features = [convert_feature_metadata(feature) for feature in build_run.features.iterator()]

    return view_models.BuildRunReport(convert_build_metadata(build_run), features)


def convert_build_metadata(build_run):
    """Convert build run to build run metadata"""
    return view_models.BuildRunMetadata(build_run.build_name, build_run.build_number,
                                        build_run.build_at, build_run.passed())


def convert_feature_metadata(feature):
    """Convert feature to its metadata"""
    return view_models.Statement(feature.name, feature.description)


def convert_feature_report(feature, build):
    """Convert dao feature to feature report for view purposes"""
    definitions = list(feature.scenario_definitions.iterator())
    bg = _find_background(definitions)
    converted_bg = None
    bg_steps = []
    converted_definitions = []

    if bg is not None:
        converted_bg = view_models.ScenarioDefinitionReport(bg.name, bg.descriiption, None,
                                                            view_models.ScenarioType.BACKGROUND)

        step_definitions = [convert_step_definition(step) for step in bg.step_definitions]
        for run in bg.scenario_runs:
            bg_steps.append(convert_step_runs(step_definitions, run.step_runs))

    bg_steps_cnt = len(bg_steps)
    run_index = 0

    for definition in definitions:
        if definition.type != 'BACKGROUND':
            converted = convert_scenario_definition(definition)
            converted_definitions.append(converted)

            if bg_steps_cnt > 0:
                for run in converted.runs:
                    run.bg_steps = bg_steps[run_index]
                    run_index += 1

    build_meta = convert_build_metadata(build)
    return view_models.FeatureReport(feature.name, feature.description, converted_definitions, converted_bg, build_meta)


def convert_scenario_definition(definition):
    """Convert scenario definition to view scenario definition"""
    runs = convert_scenario_runs(definition)
    return view_models.ScenarioDefinitionReport(definition.name, definition.description, runs,
                                                view_models.ScenarioType.from_string(definition.type))


def convert_step_definition(step):
    """Convert dao step definition to view step definition"""
    return view_models.StepDefinition(step.name, None, step.keyword)


def convert_scenario_runs(definition):
    """Convert dao scenario run to view scenario run"""
    step_definitions = [convert_step_definition(step) for step in definition.step_definitions.iterator()]
    res = []

    for run in definition.scenario_runs.iterator():
        res.append(view_models.ScenarioRun(convert_step_runs(step_definitions, run.step_runs.iterator()), []))

    return res


def convert_step_runs(step_definitions, step_runs):
    """Convert dao steps runs to view model step runs"""
    res = []
    index = 0
    for run in step_runs:
        status = view_models.StepStatus.from_string(run.status)
        res.append(view_models.StepRun(step_definitions[index], status, run.duration, run.error_msg))
        index += 1

    return res


def convert_build_run_statistics(build_run):
    """
    From provided build run create statistics object.

    :param build_run: to convert
    :return: view object to present statistics
    """
    feature_statistics = []

    for feature in build_run.features.iterator():
        step_cnt = 0
        step_run_cnt = 0
        step_passed_cnt = 0
        for definition in feature.scenario_definitions.iterator():
            print(definition.step_definitions.count())
            for scenario_run in definition.scenario_runs.iterator():
                for step_run in scenario_run.step_runs.iterator():
                    step_run_cnt += 1
                    if step_run.passed():
                        step_passed_cnt += 1
            step_cnt += definition.step_definitions.count()
        st = view_models.FeatureStatistic(feature.name, step_cnt, step_run_cnt, step_passed_cnt)
        feature_statistics.append(st)

    return view_models.BuildRunStatistics(convert_build_metadata(build_run), feature_statistics)


def convert_development_over_time(builds):
    """
    Convert builds of one project to view models.

    :param builds: to convert
    :return: list of view model objects for statistics purposes
    """
    res = []

    for build in builds:
        features = 0
        runs = 0
        definitions = 0
        steps = 0
        passed_steps = 0
        features_passed = 0
        for feature in build.features.iterator():
            features += 1
            feature_passed_steps = 0
            feature_steps = 0
            for definition in feature.scenario_definitions.iterator():
                definitions += 1
                for run in definition.scenario_runs.iterator():
                    runs += 1
                    for step in run.step_runs.iterator():
                        steps += 1
                        feature_steps +=1
                        if step.status == models.StepStatus[0][1]:
                            passed_steps += 1
                            feature_passed_steps += 1
            if feature_passed_steps == feature_steps:
                features_passed += 1
        meta = view_models.BuildRunMetadata(build.build_name, build.build_number, build.build_at, features_passed == features)
        res.append(view_models.BuildOverTimeDevelopmentStatistics(steps, features, features_passed, passed_steps, meta))

    return res


def _find_background(definitions):
    """
    Find background within definitions.

    :param definitions: to search by
    :return: background instance or None if not found
    """
    for x in definitions:
        if x.type == models.ScenarioType[2][1]:
            return x
    return None





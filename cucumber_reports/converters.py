from . import view_models


def convert_build_run(build_run):
    print("build run")
    print(build_run)
    print(build_run.features)
    """Convert dao build run to view build run"""
    features = [convert_feature_metadata(feature) for feature in build_run.features.all()]
    meta = view_models.BuildRunMetadata(build_run.build_name, build_run.build_number, build_run.build_at)

    return view_models.BuildRunReport(meta, build_run.passed(), features)


def convert_feature_metadata(feature):
    return view_models.FeatureMetadata(feature.name, feature.passed())


def convert_feature_report(feature):
    """Convert dao feature to feature report for view purposes"""
    bg = find_background(feature.scenario_definitions)
    converted_bg = None
    bg_steps = []
    definitions = []

    if bg is not None:
        converted_bg = view_models.ScenarioDefinitionReport(bg.name, bg.descriiption, None,
                                                            view_models.ScenarioType.BACKGROUND, True)
        for run in bg.scenario_runs:
            bg_steps.append(convert_step_runs(run.step_runs))

    bg_steps_cnt = len(bg_steps)
    run_index = 0

    for definition in feature.scenario_definitions:
        if definition.type != 'BACKGROUND':
            converted = convert_scenario_definition(definition)
            definitions.append(converted)

            if bg_steps_cnt > 0:
                for run in converted.runs:
                    run.bg_steps = bg_steps[run_index]
                    run_index += 1

    return view_models.FeatureReport(feature.name, feature.description, definitions, converted_bg)


def convert_scenario_definition(definition):
    """Convert scenario definition to view scenario definition"""
    runs = [convert_scenario_run(run) for run in definition.scenario_runs]
    step_definitions = [convert_step_definition(step) for step in definition.step_definitions]

    return view_models.ScenarioDefinitionReport(definition.name, definition.description, runs,
                                          view_models.ScenarioType.from_string(definition.type), step_definitions)


def convert_step_definition(step):
    """Convert dao step definition to view step definition"""
    return view_models.StepDefinition(step.name, None, step.keyword)


def convert_scenario_run(scenario_run):
    """Convert dao scenario run to view scenario run"""
    return view_models.ScenarioRun(convert_step_runs(scenario_run.step_runs), [])


def convert_step_runs(step_runs):
    """Convert dao steps runs to view model step runs"""
    res = []
    for run in step_runs:
        status = view_models.StepStatus.from_string(run.status)
        res.append(view_models.StepRun(status, status == view_models.StepStatus.PASSED, run.duration, run.error_msg))

    return res


def find_background(definitions):
    """Find background within definitions. If not present return None"""
    for x in definitions:
        if x.type == 'BACKGROUND':
            return x
    return None





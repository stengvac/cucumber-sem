from cucumber_reports import models
from . import view_models

def convert_build_run(build_run):
    features = [convert_feature(feature) for feature in build_run.features]

    return view_models.BuildRun(build_run.build_name, build_run.build_number, build_run.build_at, features)

def convert_feature(feature):
    bg = find_background(feature.scenario_definitions)
    converted_bg = None
    if bg is not None:
        converted_bg = view_models.ScenarioDefinition(bg.name, bg.descriiption, None, view_models.ScenarioType.BACKGROUND)

    return view_models.Feature(feature.name, feature.description, )

def convert_scenario_definition(definition):
    runs = [convert_scenario_run(run) for run in definition.scenario_runs]



    return view_models.ScenarioDefinition(definition.name, definition.description, runs,
                                          view_models.ScenarioType.from_string(definition.type),
                                          )
def convert_step_definition(step):
    return view_models.StepDefinition(step.name, None, step.keyword)

def convert_scenario_run(scenario_run):
    return view_models.ScenarioRun()

def

def find_background(definitions):
    for x in definitions:
        if x.type == 'BACKGROUND':
            return x
    return None
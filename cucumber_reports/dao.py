from . import models
from .converters import *


def _find_build_run(name, number):
    runs = models.BuildRun.objects.filter(build_name=name, build_number=number)

    if runs.count() == 1:
        return runs.first()
    return None


def find_build_run(name, number):
    run = _find_build_run(name, number)
    if run is None:
        return None
    return convert_build_run(run)


def find_feature(build_name, build_number, feature_name):
    build = _find_build_run(build_name, build_number)

    for feature in build.features.iterator():
        if feature.name == feature_name:
            return convert_feature_report(feature, build)

    return None


def find_n_build_runs(times):

    runs = models.BuildRun.objects.all()#.aggregate('build_name').order_by('build_number')
    res = []
    last_run = None
    name = None
    same = 0

    for run in runs:
        meta = convert_build_metadata(run)
        if name != run.build_name:
            name = run.build_name
            last_run = view_models.OverViewReport(name)
            last_run.runs.append(meta)
            res.append(last_run)
            same = 0
        else:
            same += 1
            if same < times:
                last_run.runs.append(meta)

    return res


def development_over_time(build_name):
    builds = models.BuildRun.objects.all().filter(build_name=build_name)

    res = []

    for build in builds:
        features = 0
        runs = 0
        definitions = 0
        steps = 0
        passed_steps = 0
        for feature in build.features:
            features += 1
            for definition in feature.scenario_definitions:
                definitions += 1
                for run in definition.scenario_runs:
                    runs += 1
                    for step in run.step_runs:
                        steps += 1
                        if step.status == models.StepStatus[0][1]:
                            passed_steps += 1
        meta = view_models.BuildRunMetadata(build.build_name, build.build_number, build.build_at, None)
        res.append(view_models.BuildOverTimeStatistics(steps, features, 0, passed_steps, meta))

    return res


def build_run_passed(build_run):
    for feature in build_run.features:
        for sc_def in feature.scenario_definitions:
            for run in sc_def.scenario_runs:
                for step in run.step_runs:
                    if step.status != models.StepStatus[0][1]:
                        return False
    return True




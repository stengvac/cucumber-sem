from . import models
from .converters import *
from django.http import Http404


def _find_build_run(name, number):
    """
    For given args try to find eq build run.

    :param name: eq to BuildRun.build_run field
    :param number: eq to BuildRun.build_number field
    :return: build run or raise Http404 when not found
    """
    runs = models.BuildRun.objects.filter(build_name=name, build_number=number)

    if not runs or runs.count() == 0:
        raise Http404('Build run for name: ({}) and number ({}) not found.'.format(name, number))
    return runs.first()


def find_build_run(name, number):
    """
    Try to find build run for given args and convert result to view object.

    :param name: eq to BuildRun.build_run field
    :param number: eq to BuildRun.build_number field
    :return: build run or raise Http404 when not found
    """
    return convert_build_run(_find_build_run(name, number))


def find_feature(build_name, build_number, feature_name):
    """
    Try to find feature with given args.

    :param build_name: where is feature stored
    :param build_number: of build where is feature stored
    :param feature_name: inside build
    :return: feature report or raise Http404 when not found
    """
    build = _find_build_run(build_name, build_number)

    for feature in build.features.iterator():
        if feature.name == feature_name:
            return convert_feature_report(feature, build)

    raise Http404('Feature for build_name: ({}), build_number({}) and feature_name ({]) not found.'
                  .format(build_name, build_number, feature_name))


def find_n_build_runs(times):
    """
    For all project in database return max times latest runs

    :param times: max number of builds per project to include in results
    :return: list with project name and sublist with its found build runs
    """
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
    """
    For build name try to find all its build runs and transform them into data for statistics purposes.

    :param build_name: to search builds by
    :return: list of
    """
    builds = models.BuildRun.objects.all().filter(build_name=build_name).order_by('build_number')

    if not builds:
        raise Http404('Build name: ({}) does not exist.'.format(build_name))

    res = []

    for build in builds:
        features = 0
        runs = 0
        definitions = 0
        steps = 0
        passed_steps = 0
        for feature in build.features.iterator():
            features += 1
            for definition in feature.scenario_definitions.iterator():
                definitions += 1
                for run in definition.scenario_runs.iterator():
                    runs += 1
                    for step in run.step_runs.iterator():
                        steps += 1
                        if step.status == models.StepStatus[0][1]:
                            passed_steps += 1
        meta = view_models.BuildRunMetadata(build.build_name, build.build_number, build.build_at, None)
        res.append(view_models.BuildOverTimeDevelopmentStatistics(steps, features, 0, passed_steps, meta))

    return res


def build_run_statistics(name, number):
    run = _find_build_run(name, number)
    feature_statistics = []

    for feature in run.features.iterator():
        step_cnt = 0
        step_run_cnt = 0
        step_passed_cnt = 0
        for definition in feature.scenario_definitions.iterator():
            for scenario_run in definition.scenario_runs.iterator():
                for step_run in scenario_run.step_runs.iterator():
                    step_run_cnt += 1
                    if step_run.passed():
                        step_passed_cnt += 1
            step_cnt += definition.step_definitions.count()
        st = view_models.FeatureStatistic(feature.name, feature.passed(), step_cnt, step_run_cnt, step_passed_cnt)
        feature_statistics.append(st)

    return view_models.BuildRunStatistics(convert_build_metadata(run), feature_statistics)


def build_run_passed(build_run):
    for feature in build_run.features:
        for sc_def in feature.scenario_definitions:
            for run in sc_def.scenario_runs:
                for step in run.step_runs:
                    if step.status != models.StepStatus[0][1]:
                        return False
    return True



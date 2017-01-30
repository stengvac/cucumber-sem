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
    runs = models.BuildRun.objects.all()

    return convert_last_n_build_runs(runs, times)


def development_over_time(build_name):
    """
    For build name try to find all its build runs and transform them into data for statistics purposes.

    :param build_name: to search builds by
    :return: list of
    """
    builds = models.BuildRun.objects.all().filter(build_name=build_name).order_by('build_number')

    if not builds:
        raise Http404('Build name: ({}) does not exist.'.format(build_name))

    return convert_development_over_time(builds)


def build_run_statistics(name, number):
    """
    For given args try to find build run and return its statistics.

    :param name: build name
    :param number: sequential build number
    :return: statistics or throw Http404 if not found
    """
    return convert_build_run_statistics(_find_build_run(name, number))


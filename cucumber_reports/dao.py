from . import models
from .view_models.converters import *

def _find_build_run(name, number):
    return models.BuildRun.objects.get(build_name=name, build_number=number)

def find_build_run(name, number):
    convert_build_run(_find_build_run(name, number))

def find_feature(build_name, build_number, feature_name):
    build = _find_build_run(build_name, build_number)

    for feature in build.features:
        if feature.name == feature_name:
            return convert_feature(feature)

    return None

def find_all_build_runs(build_name):
    return models.BuildRun.objects.filter(build_name=build_name)
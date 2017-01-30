from cucumber_reports import dao
import pytest
from django.http import Http404
from cucumber_reports import models
from datetime import date, time, datetime

BUILD_NAME = 'dao_b_name'
BUILD_NUMBER = '14'
BUILD_AT = date(2017, 1, 29)


@pytest.mark.django_db
def test_find_build_run_intern_not_found():
    try:
        dao._find_build_run(BUILD_NAME, BUILD_NUMBER)
        assert False
    except Http404:
        assert True


@pytest.mark.django_db
def test_find_build_run_intern():
    models.BuildRun.objects.create(build_name=BUILD_NAME, build_number=BUILD_NUMBER, build_at=BUILD_AT)

    res = dao._find_build_run(BUILD_NAME, BUILD_NUMBER)

    assert res
    assert BUILD_NAME == res.build_name
    assert int(BUILD_NUMBER) == res.build_number
    assert BUILD_AT == res.build_at.date()


@pytest.mark.django_db
def test_find_feature_not_found():
    try:
        dao.find_feature(BUILD_NAME, BUILD_NUMBER, 'Fea')
        assert False
    except Http404:
        assert True

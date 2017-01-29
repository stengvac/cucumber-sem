from cucumber_reports.templatetags import filters


def test_date_filter():
    """Test conversion from datetime to string in format d. m. Y"""
    from datetime import datetime
    result = filters.convert_date(datetime.strptime('25/7/2017', '%d/%m/%Y'))

    assert '25. 07. 2017' == result


def test_success_filter_true():
    """For boolean values return their css repre"""
    result = filters.convert_success(True)

    assert 'success' == result


def test_success_filter_false():
    """For boolean values return their css repre"""
    result = filters.convert_success(False)

    assert 'danger' == result


def test_duration_filter():
    """Convert millis to timme test"""
    result = filters.convert_millis_to_time(1500)

    assert '1.500000' == result

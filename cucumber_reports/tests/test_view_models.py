from cucumber_reports import view_models, models

def test_build_run():
    metadata = view_models.BuildRunMetadata(None, 10, None, None)
    run = view_models.BuildRunReport(metadata, None)

    assert 9 == run.previous
    assert 11 == run.next


def test_step_status_from_string():
    view_statuses = [x for x in view_models.StepStatus]
    ind = 0

    for status in models.StepStatus:
        assert view_statuses[ind] == view_models.StepStatus.from_string(status[0])
        ind += 1


def test_scenario_type_from_string():
    view_types = [x for x in view_models.ScenarioType]
    ind = 0

    for status in models.ScenarioType:
        assert view_types[ind] == view_models.ScenarioType.from_string(status[0])
        ind += 1
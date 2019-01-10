import pytest

from chaosplt_experiment.storage.interface import BaseExperimentService, \
    BaseExecutionService


def test_cannot_instanciate_experiment_service_interface():
    try:
        BaseExperimentService()
    except TypeError as e:
        return
    else:
        pytest.fail("BaseExperimentService should remain abstract")


def test_cannot_instanciate_execution_service_interface():
    try:
        BaseExecutionService()
    except TypeError as e:
        return
    else:
        pytest.fail("BaseExecutionService should remain abstract")

import os
import sys

from pkg_resources import Distribution, EntryPoint, iter_entry_points, \
    working_set

from chaosplt_experiment.storage import initialize_storage, shutdown_storage


def test_loading_external_storage_implementation():
    try:
        distribution = Distribution(os.path.join(
                os.path.dirname(__file__), "fixtures"))
        experiment_entry_point = EntryPoint.parse(
            'experiment = fake_storage:MyExperimentStorage', dist=distribution)
        execution_entry_point = EntryPoint.parse(
            'execution = fake_storage:MyExecutionStorage', dist=distribution)
        distribution._ep_map = {
            'chaosplatform.storage': {
                'experiment': experiment_entry_point,
                'execution': execution_entry_point
            }
        }
        working_set.add(distribution)

        exp_storage, exec_storage = initialize_storage(
            config={"db":{"uri": "sqlite:///"}})
        assert exp_storage.__class__.__name__ == "MyExperimentStorage"
        assert exec_storage.__class__.__name__ == "MyExecutionStorage"
        assert exp_storage.some_flag == True
        assert exec_storage.some_flag == True

        shutdown_storage(exp_storage, exec_storage)
        assert exp_storage.some_flag == False
        assert exec_storage.some_flag == False

    finally:
        distribution._ep_map.clear()

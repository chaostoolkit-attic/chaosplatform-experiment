from typing import Any, Dict, NoReturn, Tuple

from chaosplt_relational_storage import get_storage, \
    configure_storage, release_storage
import pkg_resources

from .concrete import ExperimentService, ExecutionService

__all__ = ["initialize_storage", "shutdown_storage", "ExperimentStorage",
           "ExecutionStorage"]


class ExecutionStorage(ExecutionService):
    def __init__(self, config: Dict[str, Any]):
        driver = get_storage(config)
        configure_storage(driver)
        ExecutionService.__init__(self, driver)

    def release(self) -> NoReturn:
        release_storage(self.driver)


class ExperimentStorage(ExperimentService):
    def __init__(self, config: Dict[str, Any]):
        driver = get_storage(config)
        configure_storage(driver)
        ExperimentService.__init__(self, driver)

    def release(self) -> NoReturn:
        release_storage(self.driver)


def initialize_storage(config: Dict[str, Any]) \
                       -> Tuple[ExperimentStorage, ExecutionStorage]:
    experiment_storage = None
    execution_storage = None
    for plugin in pkg_resources.iter_entry_points('chaosplatform.storage'):
        if plugin.name == "experiment":
            service_class = plugin.load()
            experiment_storage = service_class(config)

        if plugin.name == "execution":
            service_class = plugin.load()
            execution_storage = service_class(config)

    if not experiment_storage:
        experiment_storage = ExperimentStorage(config)

    if not execution_storage:
        execution_storage = ExecutionStorage(config)

    return experiment_storage, execution_storage


def shutdown_storage(experiment_storage: ExperimentStorage,
                     execution_storage: ExecutionStorage) -> NoReturn:
    experiment_storage.release()
    execution_storage.release()

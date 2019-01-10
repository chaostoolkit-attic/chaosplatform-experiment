from typing import Any, Dict, NoReturn

from chaosplt_experiment.storage import ExperimentService, ExecutionService

__all__ = ["MyExperimentStorage", "MyExecutionStorage"]


class MyExperimentStorage(ExperimentService):
    def __init__(self, config: Dict[str, Any]):
        self.some_flag = True

    def release(self) -> NoReturn:
        self.some_flag = False


class MyExecutionStorage(ExecutionService):
    def __init__(self, config: Dict[str, Any]):
        self.some_flag = True

    def release(self) -> NoReturn:
        self.some_flag = False

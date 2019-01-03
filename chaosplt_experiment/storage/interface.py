from abc import ABC, abstractmethod
from uuid import UUID
from typing import Any, List, NoReturn, Union

from chaosplt_experiment.model import Experiment, Execution

__all__ = ["BaseExperimentService", "BaseExecutionService"]


class BaseExperimentService(ABC):
    @abstractmethod
    def get(self, experiment_id: Union[UUID, str]) -> Experiment:
        raise NotImplementedError()

    @abstractmethod
    def create(self, user_id: Union[UUID, str], org_id: Union[UUID, str],
               workspace_id: Union[UUID, str], experiment: Any) -> Experiment:
        return self.save(user_id, org_id, workspace_id, experiment)

    @abstractmethod
    def delete(self, experiment_id: Union[UUID, str]) -> NoReturn:
        raise NotImplementedError()

    @abstractmethod
    def has_experiment_by_id(self, experiment_id: Union[UUID, str]) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def get_by_workspace(self, workspace_id: Union[UUID, str]) \
                         -> List[Experiment]:  # noqa: E127
        raise NotImplementedError()

    @abstractmethod
    def list_by_user(self, user_id: Union[UUID, str]) -> List[Experiment]:
        raise NotImplementedError()

    @abstractmethod
    def get_by_user(self, user_id: Union[UUID, str],
                    experiment_id: Union[UUID, str]) -> Experiment:
        raise NotImplementedError()


class BaseExecutionService(ABC):
    @abstractmethod
    def get(self, execution_id: Union[UUID, str]) -> Execution:
        raise NotImplementedError()

    @abstractmethod
    def create(self, experiment_id: Union[UUID, str],
               execution: Any) -> Execution:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, execution_id: Union[UUID, str]) -> NoReturn:
        raise NotImplementedError()

    @abstractmethod
    def get_by_user(self, user_id: Union[UUID, str]) -> List[Execution]:
        raise NotImplementedError()

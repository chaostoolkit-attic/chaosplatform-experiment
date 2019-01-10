from typing import Any, Dict, List, NoReturn, Union
from uuid import UUID

from chaosplt_experiment.model import Experiment, Execution
from chaosplt_relational_storage import RelationalStorage
from chaosplt_relational_storage.db import orm_session
from .model import Experiment as ExperimentModel, Execution as ExecutionModel

from .interface import BaseExperimentService, BaseExecutionService

__all__ = ["ExperimentService", "ExecutionService"]


class ExperimentService(BaseExperimentService):
    def __init__(self, driver: RelationalStorage):
        self.driver = driver

    def get(self, experiment_id: Union[UUID, str]) -> Experiment:
        with orm_session() as session:
            experiment = ExperimentModel.load(experiment_id, session=session)
            if not experiment:
                return

            return Experiment(
                id=experiment.id,
                user_id=experiment.user_id,
                org_id=experiment.org_id,
                workspace_id=experiment.workspace_id,
                created_date=experiment.created_date,
                updated_date=experiment.updated_date,
                payload=experiment.payload,
                executions=[
                    Execution(
                        id=execution.id,
                        user_id=experiment.user_id,
                        org_id=experiment.org_id,
                        workspace_id=experiment.workspace_id,
                        experiment_id=experiment.id
                    ) for execution in experiment.executions
                ] if experiment.executions else None
            )

    def get_chaosplatform_extension(self, experiment: Any) -> Dict[str, Any]:
        extensions = experiment.setdefault("extensions", [])
        for x in extensions:
            if x.get("name") == "chaosplatform":
                return x
        extension = {"name": "chaosplatform"}
        extensions.append(extension)
        return extension

    def create(self, user_id: Union[UUID, str], org_id: Union[UUID, str],
               workspace_id: Union[UUID, str], experiment: Any) -> Experiment:
        with orm_session() as session:
            payload = experiment
            extension = self.get_chaosplatform_extension(experiment)
            experiment = ExperimentModel.create(
                user_id, org_id, workspace_id=workspace_id,
                experiment=experiment, session=session)
            session.flush()

            extension.setdefault("experiment_id", str(experiment.id))
            extension["org_id"] = str(org_id)
            extension["workspace_id"] = str(workspace_id)
            experiment.payload = payload

            return Experiment(
                id=experiment.id,
                user_id=experiment.user_id,
                org_id=experiment.org_id,
                workspace_id=experiment.workspace_id,
                created_date=experiment.created_date,
                updated_date=experiment.updated_date,
                payload=experiment.payload
            )

    def delete(self, experiment_id: Union[UUID, str]) -> NoReturn:
        with orm_session() as session:
            ExperimentModel.delete(experiment_id, session=session)

    def get_by_workspace(self, workspace_id: Union[UUID, str]) \
                         -> List[Experiment]:  # noqa: E127
        with orm_session() as session:
            experiments = []

            candidates = ExperimentModel.load_by_workspace(
                workspace_id, session=session)
            for experiment in candidates:
                experiments.append(
                    Experiment(
                        id=experiment.id,
                        user_id=experiment.user_id,
                        org_id=experiment.org_id,
                        workspace_id=experiment.workspace_id,
                        created_date=experiment.created_date,
                        updated_date=experiment.updated_date
                    )
                )
            return experiments

    def get_by_user(self, user_id: Union[UUID, str],
                    experiment_id: Union[UUID, str]) -> Experiment:
        with orm_session() as session:
            experiment = ExperimentModel.load_by_user(
                user_id, experiment_id, session=session)
            if not experiment:
                return

            return Experiment(
                id=experiment.id,
                user_id=experiment.user_id,
                org_id=experiment.org_id,
                workspace_id=experiment.workspace_id,
                created_date=experiment.created_date,
                updated_date=experiment.updated_date,
                payload=experiment.payload,
                executions=[
                    Execution(
                        id=execution.id,
                        user_id=experiment.user_id,
                        org_id=experiment.org_id,
                        workspace_id=experiment.workspace_id,
                        experiment_id=experiment.id
                    ) for execution in experiment.executions
                ] if experiment.executions else None
            )

    def list_by_user(self, user_id: Union[UUID, str]) -> List[Experiment]:
        with orm_session() as session:
            experiments = []

            candidates = ExperimentModel.list_all_by_user(
                user_id, session=session)
            for experiment in candidates:
                experiments.append(
                    Experiment(
                        id=experiment.id,
                        user_id=experiment.user_id,
                        org_id=experiment.org_id,
                        workspace_id=experiment.workspace_id,
                        created_date=experiment.created_date,
                        updated_date=experiment.updated_date
                    )
                )
            return experiments

    def has_experiment_by_id(self, experiment_id: Union[UUID, str]) -> bool:
        with orm_session() as session:
            experiment = ExperimentModel.load(experiment_id, session=session)
            return experiment is not None


class ExecutionService(BaseExecutionService):
    def __init__(self, driver: RelationalStorage):
        self.driver = driver

    def get(self, execution_id: Union[UUID, str]) -> Execution:
        with orm_session() as session:
            execution = ExecutionModel.load(execution_id, session=session)
            if not execution:
                return

            return Execution(
                id=execution.id,
                user_id=execution.user_id,
                org_id=execution.org_id,
                workspace_id=execution.workspace_id,
                experiment_id=execution.experiment_id,
                payload=execution.payload
            )

    def create(self, experiment_id: Union[UUID, str],
               execution: Any) -> Execution:
        with orm_session() as session:
            experiment = ExperimentModel.load(experiment_id, session=session)
            execution = ExecutionModel.create(
                experiment.user_id, experiment.org_id, experiment.workspace_id,
                experiment.id, execution=execution, session=session)
            session.flush()

            return Execution(
                id=execution.id,
                user_id=execution.user_id,
                org_id=execution.org_id,
                workspace_id=execution.workspace_id,
                experiment_id=execution.experiment_id,
                payload=execution.payload
            )

    def delete(self, execution_id: Union[UUID, str]) -> NoReturn:
        with orm_session() as session:
            ExecutionModel.delete(execution_id, session=session)

    def get_by_user(self, user_id: Union[UUID, str]) -> List[Execution]:
        with orm_session() as session:
            executions = []

            candidates = ExecutionModel.load_by_user(
                user_id, session=session)
            for execution in candidates:
                executions.append(
                    Execution(
                        id=execution.id,
                        user_id=execution.user_id,
                        org_id=execution.org_id,
                        workspace_id=execution.workspace_id,
                        experiment_id=execution.experiment_id,
                        payload=execution.payload
                    )
                )
            return executions

import attr
import uuid

from chaosplt_experiment.storage import ExperimentStorage, ExecutionStorage
from chaosplt_experiment.storage.concrete import ExperimentService
from chaosplt_relational_storage.db import orm_session


def test_create_experiment(experiment_storage: ExperimentStorage):
    e = experiment_storage.create(
        user_id=uuid.uuid4(),
        org_id=uuid.uuid4(),
        workspace_id=uuid.uuid4(),
        experiment={"title": "a tale of one platform"}
    )
    assert uuid.UUID(hex=e.id.hex) == e.id


def test_load_experiment(experiment_storage: ExperimentStorage):
    e = experiment_storage.create(
        user_id=uuid.uuid4(),
        org_id=uuid.uuid4(),
        workspace_id=uuid.uuid4(),
        experiment={"title": "a tale of one platform"}
    )

    fetched_exp = experiment_storage.get(e.id)
    assert e == fetched_exp


def test_load_experiment_by_user(experiment_storage: ExperimentStorage):
    user_id = uuid.uuid4()

    e = experiment_storage.create(
        user_id=user_id,
        org_id=uuid.uuid4(),
        workspace_id=uuid.uuid4(),
        experiment={"title": "a tale of one platform"}
    )

    fetched_exp = experiment_storage.get_by_user(user_id, e.id)
    assert fetched_exp == e

    fetched_exp = experiment_storage.get_by_user(uuid.uuid4(), e.id)
    assert fetched_exp is None


def test_load_experiment_list_by_user(experiment_storage: ExperimentStorage):
    user_id = uuid.uuid4()

    e = experiment_storage.create(
        user_id=user_id,
        org_id=uuid.uuid4(),
        workspace_id=uuid.uuid4(),
        experiment={"title": "a tale of one platform"}
    )
    fetched_exps = experiment_storage.list_by_user(user_id)
    assert fetched_exps[0].id == e.id
    assert fetched_exps[0].user_id == e.user_id
    assert fetched_exps[0].org_id == e.org_id
    assert fetched_exps[0].workspace_id == e.workspace_id
    assert fetched_exps[0].created_date == e.created_date
    assert fetched_exps[0].updated_date == e.updated_date
    assert fetched_exps[0].payload is None
    assert fetched_exps[0].executions is None

    fetched_exps = experiment_storage.list_by_user(uuid.uuid4())
    assert fetched_exps == []


def test_load_experiment_by_workspace(experiment_storage: ExperimentStorage):
    user_id = uuid.uuid4()
    workspace_id = uuid.uuid4()

    e = experiment_storage.create(
        user_id=user_id,
        org_id=uuid.uuid4(),
        workspace_id=workspace_id,
        experiment={"title": "a tale of one platform"}
    )

    fetched_exps = experiment_storage.get_by_workspace(workspace_id)
    assert fetched_exps[0].id == e.id
    assert fetched_exps[0].user_id == e.user_id
    assert fetched_exps[0].org_id == e.org_id
    assert fetched_exps[0].workspace_id == e.workspace_id
    assert fetched_exps[0].created_date == e.created_date
    assert fetched_exps[0].updated_date == e.updated_date
    assert fetched_exps[0].payload is None
    assert fetched_exps[0].executions is None

    fetched_exp = experiment_storage.get_by_workspace(uuid.uuid4())
    assert fetched_exp == []


def test_delete_experiment(experiment_storage: ExperimentStorage):
    user_id = uuid.uuid4()
    workspace_id = uuid.uuid4()

    e = experiment_storage.create(
        user_id=user_id,
        org_id=uuid.uuid4(),
        workspace_id=workspace_id,
        experiment={"title": "a tale of one platform"}
    )

    fetched_exp = experiment_storage.get(e.id)
    assert e == fetched_exp

    experiment_storage.delete(e.id)
    fetched_exp = experiment_storage.get(e.id)
    assert fetched_exp == None


def test_create_execution(experiment_storage: ExperimentStorage,
                          execution_storage: ExecutionStorage):
    e = experiment_storage.create(
        user_id=uuid.uuid4(),
        org_id=uuid.uuid4(),
        workspace_id=uuid.uuid4(),
        experiment={"title": "a tale of one platform"}
    )
    e = execution_storage.create(
        experiment_id=e.id,
        execution={}
    )
    assert uuid.UUID(hex=e.id.hex) == e.id


def test_load_execution(experiment_storage: ExperimentStorage,
                        execution_storage: ExecutionStorage):
    e = experiment_storage.create(
        user_id=uuid.uuid4(),
        org_id=uuid.uuid4(),
        workspace_id=uuid.uuid4(),
        experiment={"title": "a tale of one platform"}
    )
    e = execution_storage.create(
        experiment_id=e.id,
        execution={}
    )

    fetched_exp = execution_storage.get(e.id)
    assert e == fetched_exp


def test_load_execution_by_user(experiment_storage: ExperimentStorage,
                                execution_storage: ExecutionStorage):
    user_id = uuid.uuid4()
    e = experiment_storage.create(
        user_id=user_id,
        org_id=uuid.uuid4(),
        workspace_id=uuid.uuid4(),
        experiment={"title": "a tale of one platform"}
    )
    e = execution_storage.create(
        experiment_id=e.id,
        execution={}
    )

    fetched_exs = execution_storage.get_by_user(user_id)
    assert fetched_exs == [e]

    fetched_exs = execution_storage.get_by_user(uuid.uuid4())
    assert fetched_exs == []



def test_delete_execution(experiment_storage: ExperimentStorage,
                          execution_storage: ExecutionStorage):
    user_id = uuid.uuid4()
    e = experiment_storage.create(
        user_id=user_id,
        org_id=uuid.uuid4(),
        workspace_id=uuid.uuid4(),
        experiment={"title": "a tale of one platform"}
    )
    e = execution_storage.create(
        experiment_id=e.id,
        execution={}
    )


    fetched_exp = execution_storage.get(e.id)
    assert e == fetched_exp

    execution_storage.delete(e.id)
    fetched_ex = execution_storage.get(e.id)
    assert fetched_ex == None

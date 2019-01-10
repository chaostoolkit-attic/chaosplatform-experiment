import uuid

from chaosplt_experiment.storage import ExperimentStorage, ExecutionStorage
from chaosplt_experiment.storage.model import Experiment, Execution
from chaosplt_relational_storage.db import orm_session


def test_create_experiment(experiment_storage: ExperimentStorage):
    with orm_session() as session:
        e = Experiment.create(
            user_id=uuid.uuid4(),
            org_id=uuid.uuid4(),
            workspace_id=uuid.uuid4(),
            experiment={"title": "a tale of one platform"},
            session=session
        )
        session.commit()
        assert uuid.UUID(hex=e.id.hex) == e.id


def test_load_experiment(experiment_storage: ExperimentStorage):
    with orm_session() as session:
        e = Experiment.create(
            user_id=uuid.uuid4(),
            org_id=uuid.uuid4(),
            workspace_id=uuid.uuid4(),
            experiment={"title": "a tale of one platform"},
            session=session
        )
        session.commit()

        fetched_exp = Experiment.load(e.id, session)
        assert e == fetched_exp


def test_load_experiment_by_user(experiment_storage: ExperimentStorage):
    with orm_session() as session:
        user_id = uuid.uuid4()

        e = Experiment.create(
            user_id=user_id,
            org_id=uuid.uuid4(),
            workspace_id=uuid.uuid4(),
            experiment={"title": "a tale of one platform"},
            session=session
        )
        session.commit()

        fetched_exp = Experiment.load_by_user(user_id, e.id, session)
        assert fetched_exp == e

        fetched_exp = Experiment.load_by_user(uuid.uuid4(), e.id, session)
        assert fetched_exp is None


def test_load_experiment_list_by_user(experiment_storage: ExperimentStorage):
    with orm_session() as session:
        user_id = uuid.uuid4()

        e = Experiment.create(
            user_id=user_id,
            org_id=uuid.uuid4(),
            workspace_id=uuid.uuid4(),
            experiment={"title": "a tale of one platform"},
            session=session
        )
        session.commit()

        fetched_exps = Experiment.list_all_by_user(user_id, session)
        assert fetched_exps == [e]

        fetched_exps = Experiment.list_all_by_user(uuid.uuid4(), session)
        assert fetched_exps == []


def test_load_experiment_by_workspace(experiment_storage: ExperimentStorage):
    with orm_session() as session:
        workspace_id = uuid.uuid4()

        e = Experiment.create(
            user_id=uuid.uuid4(),
            org_id=uuid.uuid4(),
            workspace_id=workspace_id,
            experiment={"title": "a tale of one platform"},
            session=session
        )
        session.commit()

        fetched_exps = Experiment.load_by_workspace(workspace_id, session)
        assert fetched_exps == [e]

        fetched_exp = Experiment.load_by_workspace(uuid.uuid4(), session)
        assert fetched_exp == []


def test_delete_experiment(experiment_storage: ExperimentStorage):
    with orm_session() as session:
        e = Experiment.create(
            user_id=uuid.uuid4(),
            org_id=uuid.uuid4(),
            workspace_id=uuid.uuid4(),
            experiment={"title": "a tale of one platform"},
            session=session
        )
        session.commit()

        fetched_exp = Experiment.load(e.id, session)
        assert e == fetched_exp

        Experiment.delete(e.id, session)
        fetched_exp = Experiment.load(e.id, session)
        assert fetched_exp == None


def test_create_execution(experiment_storage: ExperimentStorage,
                          execution_storage: ExecutionStorage):
    with orm_session() as session:
        e = Experiment.create(
            user_id=uuid.uuid4(),
            org_id=uuid.uuid4(),
            workspace_id=uuid.uuid4(),
            experiment={"title": "a tale of one platform"},
            session=session
        )
        session.flush()
        e = Execution.create(
            user_id=uuid.uuid4(),
            org_id=uuid.uuid4(),
            workspace_id=uuid.uuid4(),
            experiment_id=e.id,
            execution={},
            session=session
        )
        session.commit()
        assert uuid.UUID(hex=e.id.hex) == e.id


def test_load_execution(experiment_storage: ExperimentStorage,
                        execution_storage: ExecutionStorage):
    with orm_session() as session:
        e = Experiment.create(
            user_id=uuid.uuid4(),
            org_id=uuid.uuid4(),
            workspace_id=uuid.uuid4(),
            experiment={"title": "a tale of one platform"},
            session=session
        )
        session.flush()
        e = Execution.create(
            user_id=uuid.uuid4(),
            org_id=uuid.uuid4(),
            workspace_id=uuid.uuid4(),
            experiment_id=e.id,
            execution={},
            session=session
        )
        session.commit()

        fetched_exp = Execution.load(e.id, session)
        assert e == fetched_exp


def test_load_execution_by_user(experiment_storage: ExperimentStorage,
                                execution_storage: ExecutionStorage):
    with orm_session() as session:
        user_id = uuid.uuid4()

        e = Experiment.create(
            user_id=uuid.uuid4(),
            org_id=uuid.uuid4(),
            workspace_id=uuid.uuid4(),
            experiment={"title": "a tale of one platform"},
            session=session
        )
        session.flush()
        e = Execution.create(
            user_id=user_id,
            org_id=uuid.uuid4(),
            workspace_id=uuid.uuid4(),
            experiment_id=e.id,
            execution={},
            session=session
        )
        session.commit()

        fetched_exs = Execution.load_by_user(user_id, session)
        assert fetched_exs == [e]

        fetched_exs = Execution.load_by_user(uuid.uuid4(), session)
        assert fetched_exs == []



def test_delete_execution(experiment_storage: ExperimentStorage,
                          execution_storage: ExecutionStorage):
    with orm_session() as session:
        e = Experiment.create(
            user_id=uuid.uuid4(),
            org_id=uuid.uuid4(),
            workspace_id=uuid.uuid4(),
            experiment={"title": "a tale of one platform"},
            session=session
        )
        session.flush()
        e = Execution.create(
            user_id=uuid.uuid4(),
            org_id=uuid.uuid4(),
            workspace_id=uuid.uuid4(),
            experiment_id=e.id,
            execution={},
            session=session
        )
        session.commit()

        fetched_exp = Execution.load(e.id, session)
        assert e == fetched_exp

        Execution.delete(e.id, session)
        fetched_ex = Execution.load(e.id, session)
        assert fetched_ex == None

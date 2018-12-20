# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Any, List, NoReturn, Union
import uuid
from uuid import UUID

from chaosplt_relational_storage.db import Base
from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import relationship, defer
from sqlalchemy.orm.session import Session
from sqlalchemy_json import NestedMutable
from sqlalchemy_utils import UUIDType
from sqlalchemy_utils import JSONType as JSONB

__all__ = ["Experiment"]


class Experiment(Base):  # type: ignore
    __tablename__ = 'experiment'
    id = Column(
        UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUIDType(binary=False), nullable=False, index=True)
    org_id = Column(
        UUIDType(binary=False), nullable=False, index=True)
    workspace_id = Column(
        UUIDType(binary=False), nullable=False, index=True)
    created_date = Column(DateTime(), default=datetime.utcnow)
    updated_date = Column(
        DateTime(), default=datetime.utcnow, server_onupdate=func.now())
    suggested_experiment_id = Column(UUIDType(binary=False), index=True)
    executions = relationship(
        'Execution', backref='experiment', cascade="all, delete-orphan")
    payload = Column(NestedMutable.as_mutable(JSONB), nullable=False)

    @staticmethod
    def load(experiment_id: Union[UUID, str],
             session: Session) -> 'Experiment':
        return session.query(Experiment).filter_by(id=experiment_id).first()

    @staticmethod
    def load_by_user(user_id: Union[UUID, str],
                     experiment_id: Union[UUID, str],
                     session: Session) -> 'Experiment':
        return session.query(Experiment).\
            filter_by(id=experiment_id).\
            filter_by(user_id=user_id).first()

    @staticmethod
    def load_by_workspace(workspace_id: Union[UUID, str],
                          session: Session) -> List['Experiment']:
        return session.query(Experiment).filter_by(
            workspace_id=workspace_id).all()

    @staticmethod
    def list_all_by_user(user_id: Union[UUID, str],
                         session: Session) -> List['Experiment']:
        return session.query(Experiment).options(defer('payload')).filter_by(
            user_id=user_id).all()

    @staticmethod
    def create(user_id: Union[UUID, str], org_id: Union[UUID, str],
               workspace_id: Union[UUID, str], experiment: Any,
               session: Session) -> 'Experiment':
        experiment = Experiment(
            user_id=user_id, org_id=org_id, workspace_id=workspace_id,
            payload=experiment)
        session.add(experiment)
        return experiment

    @staticmethod
    def delete(experiment_id: Union[UUID, str],
               session: Session) -> NoReturn:
        experiment = session.query(Experiment).filter_by(
            id=experiment_id).first()

        if experiment:
            session.delete(experiment)

# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Any, List, NoReturn, Union
import uuid
from uuid import UUID

from chaosplt_relational_storage.db import Base
from sqlalchemy import Column, ForeignKey, String, UniqueConstraint, BigInteger
from sqlalchemy.orm import defer
from sqlalchemy.orm.session import Session
from sqlalchemy_utils import UUIDType
from sqlalchemy_utils import JSONType as JSONB

__all__ = ["Execution"]


class Execution(Base):  # type: ignore
    __tablename__ = 'experiment_execution'
    __table_args__ = (
        UniqueConstraint(
            'timestamp', 'experiment_id',
        ),
    )

    id = Column(
        UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUIDType(binary=False), nullable=False, index=True)
    timestamp = Column(
        BigInteger,
        default=lambda: int(datetime.utcnow().timestamp() * 1000))
    org_id = Column(UUIDType(binary=False), nullable=False, index=True)
    workspace_id = Column(
        UUIDType(binary=False), nullable=False, index=True)
    experiment_id = Column(
        UUIDType(binary=False), ForeignKey(
            'experiment.id', ondelete='CASCADE'), nullable=False)
    status = Column(String)
    payload = Column(JSONB())

    @staticmethod
    def load(execution_id: Union[UUID, str],
             session: Session) -> 'Execution':
        return session.query(Execution).filter_by(id=execution_id).first()

    @staticmethod
    def load_by_user(user_id: Union[UUID, str],
                     session: Session) -> List['Experiment']:
        return session.query(Execution).options(defer('payload')).filter_by(
            user_id=user_id).all()

    @staticmethod
    def create(user_id: Union[UUID, str], org_id: Union[UUID, str],
               workspace_id: Union[UUID, str], experiment_id: Union[UUID, str],
               execution: Any, session: Session) -> 'Execution':
        execution = Execution(
            user_id=user_id,
            org_id=org_id,
            workspace_id=workspace_id,
            experiment_id=experiment_id,
            payload=execution
        )
        session.add(execution)
        return execution

    @staticmethod
    def delete(execution_id: Union[UUID, str], session: Session) -> NoReturn:
        execution = session.query(Execution).filter_by(
            id=execution_id).first()

        if execution:
            session.delete(execution)

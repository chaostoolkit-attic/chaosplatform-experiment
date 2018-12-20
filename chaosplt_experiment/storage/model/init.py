# -*- coding: utf-8 -*-
import uuid

from chaosplt_relational_storage.db import Base
from sqlalchemy import Column, DateTime, func
from sqlalchemy_utils import UUIDType
from sqlalchemy_utils import JSONType as JSONB

__all__ = ["Init"]


class Init(Base):  # type: ignore
    __tablename__ = 'experiment_init'
    id = Column(
        UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUIDType(binary=False), nullable=False, index=True)
    received_date = Column(DateTime(), server_default=func.now())
    workspace_id = Column(
        UUIDType(binary=False), nullable=False, index=True)
    payload = Column(JSONB())

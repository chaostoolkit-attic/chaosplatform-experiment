# -*- coding: utf-8 -*-
import uuid

from chaosplt_relational_storage.db import Base
from sqlalchemy import Column, DateTime, Float, String
from sqlalchemy_utils import UUIDType
from sqlalchemy_utils import JSONType as JSONB

__all__ = ["Recommendation"]


class Recommendation(Base):  # type: ignore
    __tablename__ = 'experiment_recommendation'
    id = Column(
        UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    recommendation_type = Column(String(), index=True)
    checksum = Column(String(), nullable=False)
    last_updated = Column(DateTime())
    rating = Column(Float, default=3.0)
    meta = Column(JSONB())
    data = Column(JSONB(), nullable=False)

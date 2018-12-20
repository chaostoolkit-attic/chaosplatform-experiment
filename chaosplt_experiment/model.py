from datetime import datetime
from typing import Any, Dict, List
from uuid import UUID

import attr

__all__ = ["Experiment", "Execution"]


@attr.s
class Execution:
    id: UUID = attr.ib()
    user_id: UUID = attr.ib()
    org_id: UUID = attr.ib()
    workspace_id: UUID = attr.ib()
    experiment_id: UUID = attr.ib()
    payload: Dict[str, Any] = attr.ib(default=None)


@attr.s
class Experiment:
    id: UUID = attr.ib()
    user_id: UUID = attr.ib()
    org_id: UUID = attr.ib()
    workspace_id: UUID = attr.ib()
    created_date: datetime = attr.ib()
    updated_date: datetime = attr.ib()
    payload: Dict[str, Any] = attr.ib(default=None)
    executions: List[Execution] = attr.ib(default=None)

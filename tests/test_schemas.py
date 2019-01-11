from collections import OrderedDict
from typing import Any,     Dict
from uuid import UUID

from chaosplt_experiment.model import Execution, Experiment
from chaosplt_experiment.schemas import upload_experiment_schema, \
    experiment_schema, upload_execution_schema, execution_schema, \
    executions_schema
from flask import Flask
from marshmallow.exceptions import ValidationError
import pytest


def test_experiment_schema_requires_user_id(experiment_request: Dict[str, Any]):
    r = experiment_request.copy()
    del r["user_id"]
    
    with pytest.raises(ValidationError) as x:
        e = experiment_schema.load(r)
    assert "user_id" in x.value.messages


def test_experiment_schema_requires_org_id(experiment_request: Dict[str, Any]):
    r = experiment_request.copy()
    del r["org_id"]
    
    with pytest.raises(ValidationError) as x:
        e = experiment_schema.load(r)
    assert "org_id" in x.value.messages


def test_experiment_schema_requires_workspace_id(experiment_request: Dict[str, Any]):
    r = experiment_request.copy()
    del r["workspace_id"]
    
    with pytest.raises(ValidationError) as x:
        e = experiment_schema.load(r)
    assert "workspace_id" in x.value.messages


def test_experiment_schema(experiment_request: Dict[str, Any], user_id: UUID,
                           org_id: UUID, workspace_id: UUID, created_date: str,
                           updated_date: str, experiment: str):
    e = experiment_schema.load(experiment_request)
    assert e["user_id"] == user_id
    assert e["org_id"] == org_id
    assert e["workspace_id"] == workspace_id
    assert e["payload"] == experiment


def test_experiment_schema_no_payload(experiment_request: Dict[str, str],
                                      user_id: UUID, org_id: UUID,
                                      workspace_id: UUID, created_date: str,
                                      updated_date: str):
    r = experiment_request.copy()
    del r["payload"]

    e = experiment_schema.load(r)
    assert e["user_id"] == user_id
    assert e["org_id"] == org_id
    assert e["workspace_id"] == workspace_id
    assert "payload" not in e


def test_execution_schema(execution_request: Dict[str, str], user_id: UUID,
                          org_id: UUID, workspace_id: UUID,
                          experiment_id: UUID, journal: Dict[str, Any]):
    e = execution_schema.load(execution_request)
    assert e["user_id"] == user_id
    assert e["org_id"] == org_id
    assert e["workspace_id"] == workspace_id
    assert e["experiment_id"] == experiment_id
    assert e["payload"] == journal
    assert e["status"] == "completed"


def test_execution_schema_no_payload(execution_request: Dict[str, str],
                                     user_id: UUID, org_id: UUID,
                                     workspace_id: UUID, experiment_id: UUID,
                                     journal: Dict[str, Any]):
    r = execution_request.copy()
    del r["payload"]

    e = execution_schema.load(r)
    assert e["user_id"] == user_id
    assert e["org_id"] == org_id
    assert e["workspace_id"] == workspace_id
    assert e["experiment_id"] == experiment_id
    assert e["status"] == "completed"
    assert "payload" not in e


def test_execution_schema_requires_user_id(execution_request: Dict[str, Any]):
    r = execution_request.copy()
    del r["user_id"]
    
    with pytest.raises(ValidationError) as x:
        e = execution_schema.load(r)
    assert "user_id" in x.value.messages


def test_experiment_schema_requires_org_id(execution_request: Dict[str, Any]):
    r = execution_request.copy()
    del r["org_id"]
    
    with pytest.raises(ValidationError) as x:
        e = execution_schema.load(r)
    assert "org_id" in x.value.messages


def test_execution_schema_requires_workspace_id(execution_request: Dict[str, Any]):
    r = execution_request.copy()
    del r["workspace_id"]
    
    with pytest.raises(ValidationError) as x:
        e = execution_schema.load(r)
    assert "workspace_id" in x.value.messages


def test_execution_schema_requires_experiment_id(execution_request: Dict[str, Any]):
    r = execution_request.copy()
    del r["experiment_id"]
    
    with pytest.raises(ValidationError) as x:
        e = execution_schema.load(r)
    assert "experiment_id" in x.value.messages


def test_upload_experiment(org_id: UUID, workspace_id: UUID,
                           experiment: Dict[str, Any]):
    r = upload_experiment_schema.load({
        "org": org_id,
        "workspace": workspace_id,
        "payload": experiment
    })
    assert r["org"] == org_id
    assert r["workspace"] == workspace_id
    assert r["payload"] == experiment


def test_upload_experiment_requires_org(workspace_id: UUID,
                                        experiment: Dict[str, Any]):
    with pytest.raises(ValidationError) as x:
        upload_experiment_schema.load({
            "workspace": workspace_id,
            "payload": experiment
        })
    assert "org" in x.value.messages


def test_upload_experiment_requires_workspace(org_id: UUID,
                                              experiment: Dict[str, Any]):
    with pytest.raises(ValidationError) as x:
        upload_experiment_schema.load({
            "org": org_id,
            "payload": experiment
        })
    assert "workspace" in x.value.messages


def test_upload_experiment_requires_experiment(org_id: UUID, workspace_id: UUID):
    with pytest.raises(ValidationError) as x:
        upload_experiment_schema.load({
            "workspace": workspace_id,
            "org": org_id
        })
    assert "payload" in x.value.messages


def test_upload_execution_requires_experiment_id(journal: Dict[str, Any]):
    with pytest.raises(ValidationError) as x:
        upload_execution_schema.load({
            "payload": journal
        })
    assert "experiment_id" in x.value.messages


def test_upload_execution_requires_journal(experiment_id: UUID):
    with pytest.raises(ValidationError) as x:
        upload_execution_schema.load({
            "experiment_id": experiment_id
        })
    assert "journal" in x.value.messages

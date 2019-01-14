from datetime import datetime
import logging
from logging import StreamHandler
import os
from typing import Any, Dict, Tuple
from unittest.mock import patch, MagicMock
import uuid
from uuid import UUID

import cherrypy
from flask import Flask, request
from flask_caching import Cache
import pytest
import simplejson as json

from chaosplt_experiment.cache import setup_cache
from chaosplt_experiment.log import http_requests_logger
from chaosplt_experiment.views.web import create_app, serve_experiment_app, \
    serve_execution_app
from chaosplt_experiment.views.api import create_api, serve_experiment_api, \
    serve_execution_api
from chaosplt_experiment.service import Services, initialize_services
from chaosplt_experiment.settings import load_settings
from chaosplt_experiment.storage import ExperimentStorage, ExecutionStorage, \
    initialize_storage

cur_dir = os.path.abspath(os.path.dirname(__file__))
fixtures_dir = os.path.join(cur_dir, "fixtures")
config_path = os.path.join(fixtures_dir, 'config.toml')


@pytest.fixture
def config() -> Dict[str, Any]:
    return load_settings(config_path)


@pytest.fixture
def storages(config: Dict[str, Any]) \
             -> Tuple[ExperimentStorage, ExecutionStorage]:
    return initialize_storage(config)


@pytest.fixture
def experiment_storage(storages: Tuple[ExperimentStorage, ExecutionStorage]) \
                       -> ExperimentStorage:
    return storages[0]


@pytest.fixture
def execution_storage(storages: Tuple[ExperimentStorage, ExecutionStorage]) \
                      -> ExecutionStorage:
    return storages[1]


@pytest.fixture
def stream_handler() -> StreamHandler:
    return StreamHandler()


@pytest.fixture
def services(experiment_storage: ExperimentStorage,
             execution_storage: ExecutionStorage,
             config: Dict[str, Any]) -> Services:
    services = Services()
    services.experiment = experiment_storage
    services.execution = execution_storage
    initialize_services(services, config)
    return services


@pytest.fixture
def app(config: Dict[str, Any], services: Services,
        experiment_storage: ExperimentStorage,
        execution_storage: ExecutionStorage,
        stream_handler: StreamHandler) -> Flask:
    application = create_app(config)
    cache = setup_cache(application)
    serve_experiment_app(
        application, cache, services, experiment_storage, config,
        "/experiments", log_handler=stream_handler)
    serve_execution_app(
        application, cache, services, execution_storage, config,
        "/executions", log_handler=stream_handler)
    return application


@pytest.fixture
def api(app: Flask, config: Dict[str, Any], services: Services,
        experiment_storage: ExperimentStorage,
        execution_storage: ExecutionStorage,
        stream_handler: StreamHandler) -> Flask:
    application = create_api(config)
    cache = setup_cache(application)
    wsgiapp = http_requests_logger(application, stream_handler)
    cherrypy.tree.graft(wsgiapp, "/api/v1")
    serve_experiment_api(
        application, cache, services, experiment_storage, config,
        "/api/v1/experiments", log_handler=stream_handler)
    serve_execution_api(
        application, cache, services, execution_storage, config,
        "/api/v1/executions", log_handler=stream_handler)
    return application


@pytest.fixture
def app_cache(app: Flask) -> Cache:
    return Cache(app, config=app.config)


@pytest.fixture
def api_cache(api: Flask) -> Cache:
    return Cache(api, config=api.config)


@pytest.fixture
def user_id() -> UUID:
    return uuid.uuid4()


@pytest.fixture
def org_id() -> UUID:
    return uuid.uuid4()


@pytest.fixture
def workspace_id() -> UUID:
    return uuid.uuid4()


@pytest.fixture
def experiment_id() -> UUID:
    return uuid.uuid4()


@pytest.fixture
def created_date() -> str:
    return datetime.utcnow().isoformat()


@pytest.fixture
def updated_date() -> str:
    return datetime.utcnow().isoformat()


@pytest.fixture
def experiment() -> Dict[str, Any]:
    return {
        "title": "hello"
    }


@pytest.fixture
def experiment_request(user_id: UUID, org_id: UUID, workspace_id: UUID,
                       created_date: str, updated_date: str,
                       experiment: str) -> Dict[str, Any]:
    return {
        "id": uuid.uuid4(),
        "user_id": user_id,
        "org_id": org_id,
        "workspace_id": workspace_id,
        "created_date": created_date,
        "updated_date": updated_date,
        "payload": experiment
    }


@pytest.fixture
def journal() -> Dict[str, Any]:
    return {
        "status": "completed"
    }


@pytest.fixture
def execution_request(user_id: UUID, org_id: UUID, workspace_id: UUID,
                      experiment_id: UUID, journal: str) -> Dict[str, Any]:
    return {
        "id": uuid.uuid4(),
        "user_id": user_id,
        "org_id": org_id,
        "workspace_id": workspace_id,
        "experiment_id": experiment_id,
        "status": "completed",
        "payload": journal
    }
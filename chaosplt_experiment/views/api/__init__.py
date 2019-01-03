# -*- coding: utf-8 -*-
import logging
from logging import StreamHandler
import os
from typing import Any, Dict, Union

from flask import Blueprint, Flask, after_this_request, request, Response
from flask_caching import Cache

from chaosplt_experiment.auth import setup_jwt, setup_login
from chaosplt_experiment.schemas import setup_schemas
from chaosplt_experiment.service import Services
from chaosplt_experiment.storage import ExperimentStorage, ExecutionStorage

from .execution import api as execution_api
from .experiment import api as experiment_api

__all__ = ["create_api", "cleanup_api", "serve_experiment_api",
           "serve_execution_api"]


def create_api(config: Dict[str, Any]) -> Flask:
    app = Flask(__name__)

    app.url_map.strict_slashes = False
    app.debug = True if os.getenv('CHAOSHUB_DEBUG') else False

    logger = logging.getLogger('flask.app')
    logger.propagate = False

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.secret_key = app.config["SECRET_KEY"]

    app.config["GRPC_ADDR"] = "{}:{}".format(
        os.getenv("GRPC_LISTEN_ADDR"), os.getenv("GRPC_LISTEN_PORT"))

    app.config["CACHE_TYPE"] = os.getenv("CACHE_TYPE", "simple")
    if app.config["CACHE_TYPE"] == "redis":
        app.config["CACHE_REDIS_HOST"] = os.getenv("CACHE_REDIS_HOST")
        app.config["CACHE_REDIS_PORT"] = os.getenv("CACHE_REDIS_PORT", 6379)

    setup_jwt(app)
    setup_schemas(app)
    setup_login(app, from_jwt=True)

    return app


def cleanup_api(app: Flask):
    pass


def serve_experiment_api(app: Flask, cache: Cache, services: Services,
                         storage: ExperimentStorage, config: Dict[str, Any],
                         mount_point: str = '/api/v1/experiments',
                         log_handler: StreamHandler = None):
    register_experiment_api(app, cache, services, storage)


def serve_execution_api(app: Flask, cache: Cache, services: Services,
                        storage: ExecutionStorage, config: Dict[str, Any],
                        mount_point: str = '/api/v1/executions',
                        log_handler: StreamHandler = None):
    register_execution_api(app, cache, services, storage)


###############################################################################
# Internals
###############################################################################
def register_experiment_api(app: Flask, cache: Cache, services: Services,
                            storage: ExperimentStorage):
    patch_request(experiment_api, services, storage)
    app.register_blueprint(experiment_api, url_prefix="/experiments")


def register_execution_api(app: Flask, cache: Cache, services: Services,
                           storage: ExecutionStorage):
    patch_request(execution_api, services, storage)
    app.register_blueprint(execution_api, url_prefix="/executions")


def patch_request(bp: Blueprint, services,
                  storage: Union[ExperimentStorage, ExecutionStorage]):
    @bp.before_request
    def prepare_request():
        request.services = services
        request.storage = storage

        @after_this_request
        def clean_request(response: Response):
            request.services = None
            request.storage = None
            return response

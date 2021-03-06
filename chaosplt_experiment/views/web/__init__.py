# -*- coding: utf-8 -*-
import logging
from logging import StreamHandler
from typing import Any, Dict, Union

from flask import Blueprint, Flask, after_this_request, request, Response
from flask_caching import Cache

from chaosplt_experiment.auth import setup_jwt
from chaosplt_experiment.schemas import setup_schemas
from chaosplt_experiment.service import Services
from chaosplt_experiment.storage import ExperimentStorage, ExecutionStorage

__all__ = ["cleanup_app", "create_app", "serve_experiment_app",
           "serve_execution_app"]


def create_app(config: Dict[str, Any]) -> Flask:
    app = Flask(__name__)

    app.url_map.strict_slashes = False
    app.debug = config.get("debug", False)

    logger = logging.getLogger('flask.app')
    logger.propagate = False

    app.config["SECRET_KEY"] = config["http"]["secret_key"]
    app.secret_key = config["http"]["secret_key"]
    app.config["JWT_SECRET_KEY"] = config["jwt"]["secret_key"]
    app.config["SQLALCHEMY_DATABASE_URI"] = config["db"]["uri"]

    app.config["CACHE_TYPE"] = config["cache"].get("type", "simple")
    if app.config["CACHE_TYPE"] == "redis":
        redis_config = config["cache"]["redis"]
        app.config["CACHE_REDIS_HOST"] = redis_config.get("host")
        app.config["CACHE_REDIS_PORT"] = redis_config.get("port", 6379)
        app.config["CACHE_REDIS_DB"] = redis_config.get("db", 0)
        app.config["CACHE_REDIS_PASSWORD"] = redis_config.get("password")

    setup_jwt(app)
    setup_schemas(app)

    return app


def cleanup_app(app: Flask):
    pass


def serve_experiment_app(app: Flask, cache: Cache, services: Services,
                         storage: ExperimentStorage, config: Dict[str, Any],
                         mount_point: str = '/experiment',
                         log_handler: StreamHandler = None):
    register_experiment_views(app, cache, services, storage)


def serve_execution_app(app: Flask, cache: Cache, services: Services,
                        storage: ExperimentStorage, config: Dict[str, Any],
                        mount_point: str = '/execution',
                        log_handler: StreamHandler = None):
    register_execution_views(app, cache, services, storage)


###############################################################################
# Internals
###############################################################################
def register_experiment_views(app: Flask, cache: Cache, services: Services,
                              storage: ExperimentStorage):
    pass


def register_execution_views(app: Flask, cache: Cache, services: Services,
                             storage: ExecutionStorage):
    pass


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

import logging
from logging import StreamHandler
from typing import Any, Dict, Tuple

from chaosplt_grpc import create_grpc_server, start_grpc_server, \
    stop_grpc_server
import cherrypy
from flask import Flask
from flask_caching import Cache
from grpc import Server

from .cache import setup_cache
from .service import initialize_services, shutdown_services, Services
from .storage import ExperimentStorage, ExecutionStorage, \
    initialize_storage, shutdown_storage
from .views.api import create_api, cleanup_api, serve_experiment_api,\
    serve_execution_api
from .views.web import create_app, cleanup_app, serve_experiment_app, \
    serve_execution_app

__all__ = ["initialize_all", "release_all", "run_forever"]


def initialize_all(config: Dict[str, Any], web_app: Flask = None,
                   api_app: Flask = None, services: Services = None,
                   grpc_server: Server = None, web_cache: Cache = None,
                   api_cache: Cache = None,
                   experiment_web_mount_point: str = "/experiments",
                   execution_web_mount_point: str = "/executions",
                   experiment_api_mount_point: str = "/api/v1/experiments",
                   execution_api_mount_point: str = "/api/v1/executions",
                   access_log_handler: StreamHandler = None) \
                   -> Tuple[
                       Flask, Flask, Services, Server, ExperimentStorage,
                       ExecutionStorage]:
    access_log_handler = access_log_handler or logging.StreamHandler()

    embedded = True
    if not services:
        embedded = False
        services = Services()

    experiment_storage, execution_storage = initialize_storage(config)
    if embedded:
        services.experiment = experiment_storage
        services.execution = execution_storage

    initialize_services(services, config)

    if not web_app:
        web_app = create_app(config)
        web_cache = setup_cache(web_app)
    serve_experiment_app(
        web_app, web_cache, services, experiment_storage, config,
        experiment_web_mount_point, log_handler=access_log_handler)
    serve_execution_app(
        web_app, web_cache, services, execution_storage, config,
        execution_web_mount_point, log_handler=access_log_handler)

    if not api_app:
        api_app = create_api(config)
        api_cache = setup_cache(api_app)
    serve_experiment_api(
        api_app, api_cache, services, experiment_storage, config,
        experiment_api_mount_point, log_handler=access_log_handler)
    serve_execution_api(
        api_app, api_cache, services, execution_storage, config,
        execution_api_mount_point, log_handler=access_log_handler)

    if not grpc_server:
        srv_addr = config["GRPC_LISTEN_ADDR"]
        if srv_addr:
            grpc_server = create_grpc_server(srv_addr)
            start_grpc_server(grpc_server)
            cherrypy.log("gRPC server started on {}".format(srv_addr))

    return (web_app, api_app, services, grpc_server, experiment_storage,
            execution_storage)


def release_all(services: Services, web_app: Flask, api_app: Flask,
                grpc_server: Server, experiment_storage: ExperimentStorage,
                execution_storage: ExecutionStorage):
    if grpc_server:
        cherrypy.log("gRPC server stopping")
        stop_grpc_server(grpc_server)
        cherrypy.log("gRPC server stopped")
    cleanup_app(web_app)
    cleanup_api(api_app)
    shutdown_services(services)
    shutdown_storage(experiment_storage, execution_storage)


def run_forever(config: Dict[str, Any]):
    """
    Run and block until a signal is sent to the process.

    The application, services or gRPC server are all created and initialized
    when the application starts.
    """
    def run_stuff(config: Dict[str, Any]):
        web, api, services, grpc_server, experiment_storage, \
            execution_storage = initialize_all(config)
        cherrypy.engine.subscribe(
            'stop', lambda: release_all(
                services, web, api, grpc_server, experiment_storage,
                execution_storage),
            priority=20)

    cherrypy.engine.subscribe(
        'start', lambda: run_stuff(config), priority=80)

    cherrypy.engine.signals.subscribe()
    cherrypy.engine.start()
    cherrypy.engine.block()

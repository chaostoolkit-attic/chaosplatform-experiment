from typing import Any, Dict
from unittest.mock import ANY, MagicMock, patch

from chaosplt_experiment.service import Services
from chaosplt_experiment.server import initialize_all, release_all


@patch('chaosplt_experiment.server.create_grpc_server', autospec=True)
def test_initialize_all(create_grpc_server, config: Dict[str, Any],
                        services: Services):
    grpc_server = MagicMock()
    create_grpc_server.return_value = grpc_server

    try:
        web_app, api_app, services, grpc_server, experiment_storage, \
            execution_storage = initialize_all(config, services, None)

        assert services.experiment is not None
        assert services.execution is not None
    finally:
        release_all(
            web_app, api_app, services, grpc_server, experiment_storage,
            execution_storage)

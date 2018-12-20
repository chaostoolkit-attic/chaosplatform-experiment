from typing import Any, Dict

import attr

__all__ = ["initialize_services", "shutdown_services", "Services"]


@attr.s
class Services:
    pass


def initialize_services(services: Services, config: Dict[str, Any]):
    pass


def shutdown_services(services: Services):
    pass
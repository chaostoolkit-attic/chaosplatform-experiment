from typing import Any, Dict

import attr

__all__ = ["initialize_services", "shutdown_services", "Services"]


@attr.s
class Services:
    experiment: object = attr.ib(default=None)
    execution: object = attr.ib(default=None)


def initialize_services(services: Services, config: Dict[str, Any]):
    pass


def shutdown_services(services: Services):
    pass

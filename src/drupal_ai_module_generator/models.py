from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ServiceDef:
    name: str
    class_name: str
    description: str


@dataclass
class RouteDef:
    name: str
    path: str
    controller: str
    title: str
    permission: str


@dataclass
class ModulePlan:
    name: str
    machine_name: str
    description: str
    core_version: str = "^10 || ^11"
    dependencies: list[str] = field(default_factory=list)
    services: list[ServiceDef] = field(default_factory=list)
    routes: list[RouteDef] = field(default_factory=list)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> ModulePlan:
        services = [ServiceDef(**svc) for svc in payload.get("services", [])]
        routes = [RouteDef(**route) for route in payload.get("routes", [])]
        return cls(
            name=payload["name"],
            machine_name=payload["machine_name"],
            description=payload.get("description", ""),
            core_version=payload.get("core_version", "^10 || ^11"),
            dependencies=payload.get("dependencies", []),
            services=services,
            routes=routes,
        )

from __future__ import annotations

import json
from pathlib import Path

from drupal_ai_module_generator.generator import ModuleGenerator
from drupal_ai_module_generator.mcp_client import LocalFilesystemTool, MCPClient
from drupal_ai_module_generator.models import ModulePlan


def test_generate_module(tmp_path: Path) -> None:
    plan_payload = {
        "name": "AI Status",
        "machine_name": "ai_status",
        "description": "Expose an AI health endpoint.",
        "dependencies": ["node"],
        "services": [
            {
                "name": "ai_status.health",
                "class_name": "Drupal\\ai_status\\Service\\HealthService",
                "description": "Reports health.",
            }
        ],
        "routes": [
            {
                "name": "ai_status.health",
                "path": "/ai-status/health",
                "controller": "Drupal\\ai_status\\Controller\\HealthController::index",
                "title": "AI Health",
                "permission": "access content",
            }
        ],
    }
    plan = ModulePlan.from_dict(json.loads(json.dumps(plan_payload)))
    client = MCPClient(LocalFilesystemTool(tmp_path))
    ModuleGenerator(client).generate(plan)

    module_root = tmp_path / "ai_status"
    assert (module_root / "ai_status.info.yml").exists()
    assert (module_root / "ai_status.module").exists()
    assert (module_root / "ai_status.services.yml").exists()
    assert (module_root / "ai_status.routing.yml").exists()
    assert (module_root / "src/Service/HealthService.php").exists()
    assert (module_root / "src/Controller/HealthController.php").exists()

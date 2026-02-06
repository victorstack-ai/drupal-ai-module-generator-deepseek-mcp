from __future__ import annotations

import argparse
import json
from pathlib import Path

from drupal_ai_module_generator.generator import ModuleGenerator
from drupal_ai_module_generator.mcp_client import LocalFilesystemTool, MCPClient
from drupal_ai_module_generator.models import ModulePlan
from drupal_ai_module_generator.providers import MockProvider, provider_from_env


def _load_spec(path: Path) -> ModulePlan:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return ModulePlan.from_dict(payload)


def cmd_plan(args: argparse.Namespace) -> int:
    if args.mock:
        provider = MockProvider(plan_data=_mock_plan())
    else:
        provider = provider_from_env()
    plan = provider.plan(args.prompt)
    payload = json.dumps(plan.__dict__, default=lambda o: o.__dict__, indent=2)
    Path(args.out).write_text(payload, encoding="utf-8")
    return 0


def cmd_generate(args: argparse.Namespace) -> int:
    plan = _load_spec(Path(args.spec))
    output = Path(args.out).resolve()
    client = MCPClient(LocalFilesystemTool(output))
    generator = ModuleGenerator(client)
    generator.generate(plan)
    return 0


def _mock_plan() -> dict:
    return {
        "name": "AI Status",
        "machine_name": "ai_status",
        "description": "Expose an AI health endpoint.",
        "core_version": "^10 || ^11",
        "dependencies": [],
        "services": [
            {
                "name": "ai_status.health",
                "class_name": "Drupal\\ai_status\\Service\\HealthService",
                "description": "Reports health for the AI stack.",
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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Drupal AI module generator")
    sub = parser.add_subparsers(dest="command", required=True)

    plan = sub.add_parser("plan", help="Generate a module plan using DeepSeek R1")
    plan.add_argument("--prompt", required=True)
    plan.add_argument("--out", required=True)
    plan.add_argument("--mock", action="store_true", help="Use mock provider")
    plan.set_defaults(func=cmd_plan)

    generate = sub.add_parser("generate", help="Generate a module from a plan")
    generate.add_argument("--spec", required=True)
    generate.add_argument("--out", required=True)
    generate.set_defaults(func=cmd_generate)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import json
from pathlib import Path

from drupal_ai_module_generator.cli import build_parser


def test_plan_and_generate(tmp_path: Path) -> None:
    plan_path = tmp_path / "plan.json"
    output_dir = tmp_path / "output"

    parser = build_parser()
    args = parser.parse_args(
        [
            "plan",
            "--prompt",
            "Generate a health endpoint",
            "--out",
            str(plan_path),
            "--mock",
        ]
    )
    assert args.func(args) == 0
    assert plan_path.exists()

    plan_data = json.loads(plan_path.read_text(encoding="utf-8"))
    assert plan_data["machine_name"] == "ai_status"

    args = parser.parse_args(["generate", "--spec", str(plan_path), "--out", str(output_dir)])
    assert args.func(args) == 0
    assert (output_dir / "ai_status" / "ai_status.info.yml").exists()

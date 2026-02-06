from __future__ import annotations

import json
import os
import urllib.request
from dataclasses import dataclass
from typing import Protocol

from drupal_ai_module_generator.models import ModulePlan
from drupal_ai_module_generator.prompt import build_plan_prompt


class Provider(Protocol):
    def plan(self, prompt: str) -> ModulePlan:  # pragma: no cover - protocol
        ...


@dataclass
class DeepSeekR1Provider:
    api_key: str
    api_base: str = "https://api.deepseek.com"
    model: str = "deepseek-r1"

    def plan(self, prompt: str) -> ModulePlan:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": build_plan_prompt()},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
        }
        data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            f"{self.api_base}/v1/chat/completions",
            data=data,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=60) as response:
            body = json.loads(response.read().decode("utf-8"))

        content = body["choices"][0]["message"]["content"]
        plan_data = json.loads(content)
        return ModulePlan.from_dict(plan_data)


@dataclass
class MockProvider:
    plan_data: dict

    def plan(self, prompt: str) -> ModulePlan:
        _ = prompt
        return ModulePlan.from_dict(self.plan_data)


def provider_from_env() -> Provider:
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError("DEEPSEEK_API_KEY is required for DeepSeek provider")
    return DeepSeekR1Provider(
        api_key=api_key,
        api_base=os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com"),
        model=os.getenv("DEEPSEEK_MODEL", "deepseek-r1"),
    )

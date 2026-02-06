from __future__ import annotations


def build_plan_prompt() -> str:
    return (
        "You are a Drupal module architect. Return ONLY valid JSON with keys: "
        "name, machine_name, description, core_version, dependencies, services, routes. "
        "services is a list of {name, class_name, description}. "
        "routes is a list of {name, path, controller, title, permission}."
    )

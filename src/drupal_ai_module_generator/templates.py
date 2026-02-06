from __future__ import annotations

from drupal_ai_module_generator.models import ModulePlan


def info_yml(plan: ModulePlan) -> str:
    dependencies = "\n".join(f"  - {dep}" for dep in plan.dependencies)
    dep_block = f"dependencies:\n{dependencies}\n" if plan.dependencies else ""
    return (
        f"name: {plan.name}\n"
        f"type: module\n"
        f"description: '{plan.description}'\n"
        f"core_version_requirement: '{plan.core_version}'\n"
        f"package: Custom\n"
        f"{dep_block}"
    )


def module_file(plan: ModulePlan) -> str:
    return (
        f"<?php\n\n"
        f"/**\n"
        f" * @file\n"
        f" * {plan.name} module.\n"
        f" */\n"
    )


def services_yml(plan: ModulePlan) -> str:
    lines = ["services:"]
    for service in plan.services:
        lines.append(f"  {service.name}:")
        lines.append(f"    class: {service.class_name}")
        lines.append("    arguments: []")
    return "\n".join(lines) + "\n"


def routing_yml(plan: ModulePlan) -> str:
    lines: list[str] = []
    for route in plan.routes:
        lines.extend(
            [
                f"{route.name}:",
                f"  path: '{route.path}'",
                "  defaults:",
                f"    _controller: '{route.controller}'",
                f"    _title: '{route.title}'",
                "  requirements:",
                f"    _permission: '{route.permission}'",
            ]
        )
    return "\n".join(lines) + "\n"


def controller_php(class_name: str, method_name: str = "index") -> str:
    namespace, short_name = class_name.rsplit("\\", 1)
    return (
        "<?php\n\n"
        f"namespace {namespace};\n\n"
        "use Drupal\\Core\\Controller\\ControllerBase;\n"
        "use Symfony\\Component\\HttpFoundation\\JsonResponse;\n\n"
        f"class {short_name} extends ControllerBase\n"
        "{\n"
        f"    public function {method_name}(): JsonResponse\n"
        "    {\n"
        "        return new JsonResponse(['status' => 'ok']);\n"
        "    }\n"
        "}\n"
    )


def service_php(class_name: str, description: str) -> str:
    namespace, short_name = class_name.rsplit("\\", 1)
    return (
        "<?php\n\n"
        f"namespace {namespace};\n\n"
        f"/**\n * {description}\n */\n"
        f"class {short_name}\n"
        "{\n"
        "}\n"
    )

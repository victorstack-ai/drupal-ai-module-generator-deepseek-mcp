# Drupal AI Module Generator (DeepSeek R1 + MCP)

A pragmatic CLI that turns a short module brief into a Drupal module scaffold. It uses a DeepSeek R1 provider to produce a structured module plan and a minimal MCP-style tool layer to write files, so you can later swap in a real MCP filesystem server.

## What it does

- Builds a module plan via DeepSeek R1 (OpenAI-compatible API)
- Generates Drupal files (info, module, services, routing, controller stubs)
- Writes files through an MCP-style tool interface (local filesystem by default)

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]

# Generate a plan from a prompt (requires DeepSeek API key)
export DEEPSEEK_API_KEY=YOUR_KEY
python -m drupal_ai_module_generator.cli plan \
  --prompt "Create a module that exposes a JSON status endpoint" \
  --out plan.json

# Generate a module from a plan
python -m drupal_ai_module_generator.cli generate \
  --spec plan.json \
  --out ./output
```

## Environment variables

- `DEEPSEEK_API_KEY`: API key for DeepSeek
- `DEEPSEEK_API_BASE`: Optional API base (default `https://api.deepseek.com`)
- `DEEPSEEK_MODEL`: Optional model name (default `deepseek-r1`)

## Development

```bash
pip install -e .[dev]
pytest
ruff check .
```

## Notes

This project ships with a local MCP filesystem implementation. If you have a real MCP server, wire it into `MCPClient`.

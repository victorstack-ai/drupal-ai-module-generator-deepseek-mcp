from __future__ import annotations

from pathlib import Path

from drupal_ai_module_generator.mcp_client import LocalFilesystemTool, MCPClient


def test_mcp_write(tmp_path: Path) -> None:
    client = MCPClient(LocalFilesystemTool(tmp_path))
    client.write_file("foo/bar.txt", "hello")
    assert (tmp_path / "foo/bar.txt").read_text(encoding="utf-8") == "hello"

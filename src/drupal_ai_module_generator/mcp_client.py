from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


class MCPFilesystem(Protocol):
    def write_text(self, relative_path: str, content: str) -> None:  # pragma: no cover - protocol
        ...


@dataclass
class LocalFilesystemTool:
    base_path: Path

    def write_text(self, relative_path: str, content: str) -> None:
        target = self.base_path / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")


@dataclass
class MCPClient:
    filesystem: MCPFilesystem

    def write_file(self, relative_path: str, content: str) -> None:
        self.filesystem.write_text(relative_path, content)

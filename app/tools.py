from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Callable


ToolFn = Callable[[dict[str, Any]], Any]


def get_time(_: dict[str, Any]) -> str:
    return datetime.now(tz=timezone.utc).isoformat()


def add_numbers(payload: dict[str, Any]) -> dict[str, float]:
    a = float(payload.get("a", 0))
    b = float(payload.get("b", 0))
    return {"a": a, "b": b, "sum": a + b}


def echo(payload: dict[str, Any]) -> dict[str, Any]:
    return payload


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolFn] = {
            "get_time": get_time,
            "add_numbers": add_numbers,
            "echo": echo,
        }

    def list_tools(self) -> list[str]:
        return sorted(self._tools)

    def execute(self, action: str, payload: dict[str, Any]) -> Any:
        if action not in self._tools:
            raise ValueError(f"Unknown tool '{action}'. Available tools: {', '.join(self.list_tools())}")
        return self._tools[action](payload)

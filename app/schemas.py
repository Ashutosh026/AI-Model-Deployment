from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class AgentRequest:
    prompt: str
    context: dict[str, Any] = field(default_factory=dict)


@dataclass
class PlanStep:
    id: int
    thought: str
    action: str
    input: dict[str, Any] = field(default_factory=dict)


@dataclass
class StepResult:
    step_id: int
    action: str
    observation: Any

    def model_dump(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentResponse:
    objective: str
    plan: list[PlanStep]
    execution_log: list[StepResult]
    final_answer: str

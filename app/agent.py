from __future__ import annotations

from app.llm import LLMClient
from app.schemas import AgentResponse, PlanStep, StepResult
from app.tools import ToolRegistry


class PromptDrivenAgent:
    def __init__(self, llm_client: LLMClient | None = None, tools: ToolRegistry | None = None) -> None:
        self.llm_client = llm_client or LLMClient()
        self.tools = tools or ToolRegistry()

    def run(self, objective: str, context: dict) -> AgentResponse:
        plan = self._build_plan(objective=objective, context=context)
        execution_log: list[StepResult] = []

        for step in plan:
            observation = self.tools.execute(step.action, step.input)
            execution_log.append(
                StepResult(step_id=step.id, action=step.action, observation=observation)
            )

        final_answer = self.llm_client.summarize(
            objective=objective,
            observations=[result.model_dump() for result in execution_log],
        )

        return AgentResponse(
            objective=objective,
            plan=plan,
            execution_log=execution_log,
            final_answer=final_answer,
        )

    def _build_plan(self, objective: str, context: dict) -> list[PlanStep]:
        plan = self.llm_client.plan(objective=objective, tools=self.tools.list_tools(), context=context)
        if not plan:
            raise ValueError("LLM planner returned an empty plan.")
        return plan

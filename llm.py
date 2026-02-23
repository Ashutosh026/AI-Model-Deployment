from __future__ import annotations

import json
import os
from typing import Any


from app.schemas import PlanStep


class LLMClient:
    """Minimal LLM wrapper that returns JSON plans.

    If AI_API_URL is not configured, it falls back to a deterministic local planner.
    """

    def __init__(self) -> None:
        self.api_url = os.getenv("AI_API_URL")
        self.api_key = os.getenv("AI_API_KEY")
        self.model = os.getenv("AI_MODEL", "gpt-4o-mini")

    def plan(self, objective: str, tools: list[str], context: dict[str, Any]) -> list[PlanStep]:
        if not self.api_url:
            return self._fallback_plan(objective)

        system_prompt = (
            "You are a planning assistant. Return ONLY valid JSON: "
            "an array of steps where each item has keys id, thought, action, input. "
            f"Available actions: {tools}."
        )
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": json.dumps({"objective": objective, "context": context}),
                },
            ],
            "temperature": 0.1,
        }
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        import httpx


        with httpx.Client(timeout=20) as client:
            response = client.post(self.api_url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()

        content = data["choices"][0]["message"]["content"]
        raw_steps = json.loads(content)
        return [PlanStep(**step) for step in raw_steps]

    def summarize(self, objective: str, observations: list[dict[str, Any]]) -> str:
        if not self.api_url:
            return f"Completed objective '{objective}' in {len(observations)} steps."

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "Summarize the execution in 2-3 sentences."},
                {
                    "role": "user",
                    "content": json.dumps({"objective": objective, "observations": observations}),
                },
            ],
            "temperature": 0.2,
        }
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        with httpx.Client(timeout=20) as client:
            response = client.post(self.api_url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()

        return data["choices"][0]["message"]["content"].strip()

    def _fallback_plan(self, objective: str) -> list[PlanStep]:
        steps = [
            PlanStep(id=1, thought="Capture the original user objective.", action="echo", input={"objective": objective}),
            PlanStep(id=2, thought="Record current UTC time for execution traceability.", action="get_time", input={}),
        ]

        numbers = [float(token) for token in objective.split() if token.replace(".", "", 1).isdigit()]
        if len(numbers) >= 2:
            steps.append(
                PlanStep(
                    id=3,
                    thought="Detected numeric values in objective. Compute a sum.",
                    action="add_numbers",
                    input={"a": numbers[0], "b": numbers[1]},
                )
            )
        return steps

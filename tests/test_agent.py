from app.agent import PromptDrivenAgent


def test_agent_executes_fallback_plan() -> None:
    agent = PromptDrivenAgent()

    result = agent.run("Please add 5 and 7", context={"source": "test"})

    actions = [step.action for step in result.plan]
    assert "echo" in actions
    assert "get_time" in actions
    assert "add_numbers" in actions
    assert "Completed objective" in result.final_answer


def test_agent_without_numbers_skips_addition() -> None:
    agent = PromptDrivenAgent()

    result = agent.run("Summarize deployment status", context={})

    actions = [step.action for step in result.plan]
    assert "add_numbers" not in actions

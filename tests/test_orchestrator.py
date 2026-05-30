from agentic_lab.agents import MultiAgentOrchestrator
from agentic_lab.models import MockProvider
from agentic_lab.schemas import LLMConfig


def test_orchestrator_runs_with_mock_provider():
    provider = MockProvider(LLMConfig(provider="mock", model="mock-agent"))
    result = MultiAgentOrchestrator(provider).run("Build OpenClaw MCP Claude Ollama multi-agent demo")
    assert result.provider == "mock"
    assert len(result.agent_results) == 4
    assert "Recommended architecture" in result.final_answer
    assert result.risks

from __future__ import annotations

from .models import BaseLLMProvider
from .schemas import AgentResult, AgentSpec, ChatMessage, OrchestrationResult
from .tools import analyze_agent_request, generate_repo_blueprint, security_review

DEFAULT_AGENTS = [
    AgentSpec(
        name="Planner",
        role="Principal Agentic AI Architect",
        objective="Break the goal into deliverables and architecture decisions.",
        guardrails=["Be concrete", "Prefer shippable outputs"],
    ),
    AgentSpec(
        name="MCP Integrator",
        role="MCP Platform Engineer",
        objective="Map the workflow into MCP tools, contracts, and invocation boundaries.",
        guardrails=["Keep tools narrow", "Avoid unrestricted execution"],
    ),
    AgentSpec(
        name="Model Runtime Engineer",
        role="LLM Systems Engineer",
        objective="Decide how Claude and OSS models are selected, configured, and tested.",
        guardrails=["Keep provider abstraction", "Support local-first demos"],
    ),
    AgentSpec(
        name="Security Reviewer",
        role="AI Security Engineer",
        objective="Identify prompt-injection, tool-use, secrets, and access-control risks.",
        guardrails=["No secrets in prompts", "No destructive tools by default"],
    ),
]


class MultiAgentOrchestrator:
    """A small, readable multi-agent loop for portfolio and interview demos."""

    def __init__(self, provider: BaseLLMProvider, agents: list[AgentSpec] | None = None):
        self.provider = provider
        self.agents = agents or DEFAULT_AGENTS

    def run(self, task: str) -> OrchestrationResult:
        analysis = analyze_agent_request(task)
        blueprint = generate_repo_blueprint(task)
        prior_outputs: list[str] = []
        agent_results: list[AgentResult] = []

        for agent in self.agents:
            system_prompt = (
                f"You are {agent.name}, acting as {agent.role}. "
                f"Objective: {agent.objective}. "
                f"Guardrails: {'; '.join(agent.guardrails)}."
            )
            user_prompt = (
                f"Task: {task}\n\n"
                f"Request analysis: {analysis}\n\n"
                f"Repo blueprint: {blueprint}\n\n"
                f"Previous agent outputs: {prior_outputs[-3:]}\n\n"
                "Return a concise, implementation-oriented contribution."
            )
            output = self.provider.generate(
                [
                    ChatMessage(role="system", content=system_prompt),
                    ChatMessage(role="user", content=user_prompt),
                ]
            )
            prior_outputs.append(f"{agent.name}: {output}")
            agent_results.append(
                AgentResult(
                    agent=agent.name,
                    summary=agent.objective,
                    output=output,
                )
            )

        security = security_review("\n".join(prior_outputs) + "\n" + task)
        final_answer = self._compose_final(task, analysis, blueprint, agent_results, security)
        return OrchestrationResult(
            task=task,
            provider=self.provider.config.provider,
            model=self.provider.config.model,
            agent_results=agent_results,
            final_answer=final_answer,
            risks=[item["risk"] for item in security["risks"]],
            next_steps=[
                "Connect the MCP server to Claude Desktop or another MCP-compatible client.",
                "Wire the webhook adapter to the selected OpenClaw channel/plugin.",
                "Run the same workflow using Claude and an Ollama-hosted OSS model, then compare outputs.",
            ],
        )

    @staticmethod
    def _compose_final(task: str, analysis: dict, blueprint: dict, results: list[AgentResult], security: dict) -> str:
        agent_lines = "\n".join(f"- {r.agent}: {r.summary}" for r in results)
        risk_lines = "\n".join(f"- {risk['risk']} → {risk['mitigation']}" for risk in security["risks"][:4])
        return (
            f"# Agentic Implementation Blueprint\n\n"
            f"## Task\n{task}\n\n"
            f"## Detected capabilities\n{', '.join(analysis['capabilities_detected']) or 'general agentic AI'}\n\n"
            f"## Recommended architecture\n{analysis['recommended_architecture']}\n\n"
            f"## Components\n" + "\n".join(f"- {c}" for c in blueprint["components"]) + "\n\n"
            f"## Specialist agents used\n{agent_lines}\n\n"
            f"## Top safety controls\n{risk_lines}\n"
        )

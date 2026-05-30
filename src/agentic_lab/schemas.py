from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

ProviderName = Literal["mock", "claude", "ollama"]


@dataclass(frozen=True)
class ChatMessage:
    role: Literal["system", "user", "assistant"]
    content: str


@dataclass(frozen=True)
class LLMConfig:
    provider: ProviderName = "mock"
    model: str = "mock-agent"
    temperature: float = 0.2
    max_tokens: int = 1200


@dataclass(frozen=True)
class AgentSpec:
    name: str
    role: str
    objective: str
    guardrails: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class AgentResult:
    agent: str
    summary: str
    output: str


@dataclass(frozen=True)
class OrchestrationResult:
    task: str
    provider: str
    model: str
    agent_results: list[AgentResult]
    final_answer: str
    risks: list[str]
    next_steps: list[str]

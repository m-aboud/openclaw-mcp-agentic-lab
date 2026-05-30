from __future__ import annotations

import os
from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Any, cast

import httpx

from .schemas import ChatMessage, LLMConfig


class BaseLLMProvider(ABC):
    """Small provider abstraction so the same agent loop can run on Claude or OSS models."""

    def __init__(self, config: LLMConfig):
        self.config = config

    @abstractmethod
    def generate(self, messages: Iterable[ChatMessage]) -> str:
        raise NotImplementedError


class MockProvider(BaseLLMProvider):
    """Deterministic provider for demos, tests, and offline portfolio review."""

    def generate(self, messages: Iterable[ChatMessage]) -> str:
        user_text = "\n".join(m.content for m in messages if m.role == "user")
        return (
            "Mock agent response:\n"
            "- Extracted goal: build a production-minded multi-agent AI workflow.\n"
            "- Recommended path: OpenClaw gateway + MCP tool server + Claude/Ollama runtime switch.\n"
            "- Key engineering concern: tool safety, observability, and deterministic fallbacks.\n"
            f"- Input fingerprint: {abs(hash(user_text)) % 100000}"
        )


class ClaudeProvider(BaseLLMProvider):
    """Claude Messages API provider."""

    def generate(self, messages: Iterable[ChatMessage]) -> str:
        try:
            import anthropic
        except ImportError as exc:  # pragma: no cover - dependency is optional at runtime
            raise RuntimeError("Install anthropic or use --provider mock/ollama") from exc

        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is required for ClaudeProvider")

        system_parts: list[str] = []
        api_messages: list[dict[str, str]] = []
        for message in messages:
            if message.role == "system":
                system_parts.append(message.content)
            else:
                api_messages.append({"role": message.role, "content": message.content})

        client = anthropic.Anthropic(api_key=api_key)
        create_kwargs: dict[str, Any] = {
            "model": self.config.model,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature,
            "messages": cast(Any, api_messages),
        }
        system_text = "\n\n".join(system_parts)
        if system_text:
            create_kwargs["system"] = system_text

        response = client.messages.create(**create_kwargs)
        return "\n".join(getattr(block, "text", "") for block in response.content).strip()


class OllamaProvider(BaseLLMProvider):
    """Local/open-source model provider via Ollama chat API."""

    def generate(self, messages: Iterable[ChatMessage]) -> str:
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
        payload = {
            "model": self.config.model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "stream": False,
            "options": {"temperature": self.config.temperature},
        }
        with httpx.Client(timeout=90) as client:
            response = client.post(f"{base_url}/api/chat", json=payload)
            response.raise_for_status()
            data = response.json()
        return data.get("message", {}).get("content", "").strip()


def build_provider(provider: str | None = None, model: str | None = None) -> BaseLLMProvider:
    selected = (provider or os.getenv("AGENTIC_LAB_PROVIDER") or "mock").lower()
    if selected == "claude":
        model_name = model or os.getenv("CLAUDE_MODEL") or "claude-opus-4-8"
        return ClaudeProvider(LLMConfig(provider="claude", model=model_name))
    if selected == "ollama":
        model_name = model or os.getenv("OLLAMA_MODEL") or "qwen2.5:7b"
        return OllamaProvider(LLMConfig(provider="ollama", model=model_name))
    return MockProvider(LLMConfig(provider="mock", model=model or "mock-agent"))

from __future__ import annotations

import re
from dataclasses import asdict

from .schemas import AgentSpec


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def analyze_agent_request(request: str) -> dict:
    """Classify an agentic AI request and extract relevant technical signals."""
    clean = normalize_text(request)
    lowered = clean.lower()
    capabilities = []
    for key in ["openclaw", "mcp", "claude", "ollama", "qwen", "llama", "rag", "multi-agent", "security", "docker"]:
        if key in lowered:
            capabilities.append(key)

    complexity = "high" if len(capabilities) >= 5 else "medium" if len(capabilities) >= 3 else "low"
    return {
        "request": clean,
        "complexity": complexity,
        "capabilities_detected": capabilities,
        "recommended_architecture": "gateway -> orchestrator -> model provider -> MCP tools",
        "acceptance_criteria": [
            "Runs locally without paid APIs using mock provider",
            "Can switch to Claude through environment configuration",
            "Can switch to Ollama for OSS models",
            "Exposes at least four MCP tools",
            "Includes security review and tests",
        ],
    }


def generate_repo_blueprint(goal: str, model_stack: str = "Claude + Ollama", channel: str = "OpenClaw") -> dict:
    """Generate a GitHub-ready architecture blueprint for an agentic AI showcase."""
    goal = normalize_text(goal)
    return {
        "name": "openclaw-mcp-agentic-lab",
        "goal": goal,
        "channel_gateway": channel,
        "model_stack": model_stack,
        "components": [
            "OpenClaw-facing gateway profile and config",
            "FastAPI webhook adapter",
            "Multi-agent orchestrator",
            "MCP server exposing deterministic tools",
            "Claude provider",
            "Ollama provider for OSS models",
            "Security review workflow",
            "Docker and CI pipeline",
        ],
        "folders": {
            "src/agentic_lab": "Python package with agents, tools, providers, API and MCP server",
            "configs": "OpenClaw and Claude Desktop configuration examples",
            "docs": "Architecture, security, setup, and interview talk track",
            "tests": "Unit tests for tools and orchestration",
            "examples": "Sample requests and outputs",
        },
        "demo_commands": [
            "agentic-lab run-demo --provider mock",
            "agentic-lab run-demo --provider ollama --model qwen2.5:7b",
            "agentic-lab mcp-server",
            "uvicorn agentic_lab.api:app --port 8080",
        ],
    }


def security_review(architecture_text: str) -> dict:
    """Review an agentic workflow for common MCP and tool-use risks."""
    text = architecture_text.lower()
    risks = [
        {
            "risk": "Prompt injection through channel messages or documents",
            "mitigation": "Separate user content from system instructions and require tool-specific validation.",
        },
        {
            "risk": "Over-permissive MCP tools",
            "mitigation": "Expose narrow tools only; avoid shell execution and unrestricted file writes.",
        },
        {
            "risk": "Secrets leakage in logs or model context",
            "mitigation": "Never send API keys, tokens, or private config to the model; redact logs.",
        },
        {
            "risk": "Model/provider lock-in",
            "mitigation": "Keep provider abstraction so Claude and OSS models can be swapped.",
        },
    ]
    if "openclaw" in text:
        risks.append(
            {
                "risk": "Messaging-channel impersonation or unauthorized sender access",
                "mitigation": "Use channel allowlists, mention rules, and per-sender/session isolation.",
            }
        )
    if "mcp" in text:
        risks.append(
            {
                "risk": "Tool poisoning or ambiguous tool descriptions",
                "mitigation": "Use explicit tool names, schemas, versioning, and human review for sensitive actions.",
            }
        )
    return {"risk_count": len(risks), "risks": risks}


def create_openclaw_agent_prompt(role: str, context: str) -> dict:
    """Create a portable OpenClaw-facing agent operating profile."""
    role = normalize_text(role)
    context = normalize_text(context)
    spec = AgentSpec(
        name="OpenClaw MCP Agentic Engineer",
        role=role,
        objective="Route user requests into safe multi-agent workflows using MCP tools and Claude/OSS models.",
        guardrails=[
            "Ask for confirmation before destructive or external actions.",
            "Never expose secrets, tokens, or private credentials.",
            "Use MCP tools only when they directly support the task.",
            "Prefer deterministic outputs for repo, architecture, and security planning.",
        ],
    )
    return {
        "agent": asdict(spec),
        "system_prompt": (
            f"You are {spec.name}. Your role is {role}. Context: {context}. "
            "When a user sends a task through OpenClaw, classify it, choose the right specialist agent, "
            "use MCP tools when useful, and return concise engineering-grade output. "
            "Do not run destructive actions without explicit approval."
        ),
    }

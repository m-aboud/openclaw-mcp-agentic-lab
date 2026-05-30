from __future__ import annotations

import os
from typing import Any

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from .agents import MultiAgentOrchestrator
from .models import build_provider

app = FastAPI(
    title="OpenClaw MCP Agentic Lab API",
    description="Webhook-style adapter for routing OpenClaw channel messages into a multi-agent workflow.",
    version="0.1.0",
)


class OpenClawMessage(BaseModel):
    text: str = Field(..., description="User message text from the channel gateway")
    sender: str | None = Field(default=None, description="Gateway/channel sender identifier")
    channel: str | None = Field(default="webchat", description="Channel name such as telegram, whatsapp, slack")
    metadata: dict[str, Any] = Field(default_factory=dict)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "openclaw-mcp-agentic-lab"}


@app.post("/openclaw/message")
def handle_openclaw_message(payload: OpenClawMessage, x_agentic_lab_key: str | None = Header(default=None)) -> dict:
    expected_key = os.getenv("AGENTIC_LAB_API_KEY")
    if expected_key and expected_key != "change-me-local-dev" and x_agentic_lab_key != expected_key:
        raise HTTPException(status_code=401, detail="Invalid adapter key")

    provider = build_provider()
    orchestrator = MultiAgentOrchestrator(provider)
    result = orchestrator.run(payload.text)
    return {
        "reply": result.final_answer,
        "provider": result.provider,
        "model": result.model,
        "channel": payload.channel,
        "sender": payload.sender,
        "risks_detected": result.risks,
        "next_steps": result.next_steps,
    }

# OpenClaw Setup Concept

This repo does not vendor OpenClaw. It provides an OpenClaw-facing agent profile and an adapter API that can be connected to a gateway/channel deployment.

## Local OpenClaw idea

1. Install and onboard OpenClaw according to the official docs.
2. Start this repo API:

```bash
uvicorn agentic_lab.api:app --host 0.0.0.0 --port 8080
```

3. Use `configs/openclaw.agent.md` as the agent instruction profile.
4. Use `configs/openclaw.example.json5` as a safe starting point for channel allowlists and mention rules.

## Demo without OpenClaw

You can still prove the engineering concept locally:

```bash
agentic-lab run-demo --provider mock
curl -X POST http://127.0.0.1:8080/openclaw/message \
  -H 'Content-Type: application/json' \
  -d '{"text":"Build an OpenClaw + MCP + Claude/Ollama multi-agent workflow","sender":"demo","channel":"webchat"}'
```

## Interview explanation

> “I kept the agent logic decoupled from the gateway. OpenClaw can handle channels and sessions, while this repo provides the orchestration, MCP tools, model providers, and security controls.”

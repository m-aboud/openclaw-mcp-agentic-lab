# Architecture

## Design goal

This project demonstrates a practical agentic AI platform pattern rather than a chatbot-only demo.

## Core pattern

```mermaid
sequenceDiagram
    participant User
    participant OpenClaw as OpenClaw Gateway
    participant API as Webhook Adapter
    participant Orchestrator
    participant Claude as Claude API
    participant Ollama as Ollama / OSS Model
    participant MCP as MCP Server

    User->>OpenClaw: Sends task from messaging channel
    OpenClaw->>API: POST /openclaw/message
    API->>Orchestrator: Run multi-agent workflow
    Orchestrator->>Claude: Optional high-reasoning call
    Orchestrator->>Ollama: Optional local model call
    Orchestrator->>MCP: Call deterministic tools
    MCP-->>Orchestrator: Structured tool result
    Orchestrator-->>API: Final answer + risks + next steps
    API-->>OpenClaw: Reply payload
    OpenClaw-->>User: Message response
```

## Components

### 1. Gateway layer

OpenClaw is treated as the channel gateway. It handles user access through messaging surfaces such as Telegram, WhatsApp, Slack, or WebChat.

### 2. Adapter layer

`agentic_lab.api` exposes `/openclaw/message`. This keeps the agentic system decoupled from any one channel implementation.

### 3. Orchestration layer

`MultiAgentOrchestrator` runs four specialist agents:

| Agent | Responsibility |
|---|---|
| Planner | Breaks the user goal into deliverables |
| MCP Integrator | Maps tools, schemas, and integration boundaries |
| Model Runtime Engineer | Chooses Claude vs OSS model strategy |
| Security Reviewer | Reviews prompt-injection, tool abuse, secrets, and access risks |

### 4. Model provider layer

Provider selection is controlled by environment variables or CLI flags.

| Provider | Use case |
|---|---|
| `mock` | Deterministic demo and tests |
| `claude` | Advanced reasoning using Anthropic Claude |
| `ollama` | Local OSS models such as Qwen, Llama, Mistral, DeepSeek, Gemma |

### 5. MCP layer

`agentic_lab.mcp_server` exposes tools that can be consumed by MCP-compatible clients.

## Why this is strong for interviews

It shows the candidate understands:

- agent gateway/channel separation
- tool protocol standardization
- model abstraction
- local-first AI
- production safety controls
- tests and deployability

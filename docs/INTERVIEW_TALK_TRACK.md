# Interview Talk Track

## 30-second pitch

I built a portfolio project that connects an OpenClaw-style messaging gateway to a Python multi-agent orchestration layer. The system exposes tools through MCP and supports both Claude and local OSS models through Ollama. It includes a deterministic mock provider for tests, a FastAPI adapter, Docker setup, CI, and a security-focused MCP threat model.

## How I would answer: “Have you dealt with MCP?”

Yes. I created a Python MCP server that exposes structured tools for request analysis, repository blueprint generation, OpenClaw agent prompt creation, and security review. I understand MCP as the standard interface between AI clients and external tools, and I designed the tools to be narrow, auditable, and safe by default.

## How I would answer: “Claude or OSS models?”

Both. The repo has a provider abstraction that can call Claude through Anthropic’s Messages API or local/open-source models through Ollama. This makes the workflow portable across commercial and self-hosted models such as Qwen, Llama, Mistral, DeepSeek, and Gemma.

## How I would answer: “OpenClaw?”

I understand OpenClaw as the agent gateway/channel layer. My demo keeps the agent runtime separate from the gateway by exposing a webhook adapter and an OpenClaw-facing agent profile. That means the same orchestrator can work behind Telegram, WhatsApp, Slack, WebChat, or any OpenClaw-supported channel.

## Strong resume bullet

Built an OpenClaw-facing multi-agent AI platform integrating a Python MCP tool server, Claude API provider, and Ollama/OSS model runtime; implemented role-based orchestration, secure tool boundaries, Docker deployment, and CI-tested workflows for agentic engineering demos.

## 2-minute technical explanation

The project has five layers. First, OpenClaw handles channel access. Second, a FastAPI adapter receives messages and normalizes the payload. Third, a multi-agent orchestrator routes the task to specialist agents: planner, MCP integrator, model runtime engineer, and security reviewer. Fourth, an MCP server exposes deterministic tools that produce structured outputs. Fifth, the model provider abstraction allows the same workflow to run with Claude, Ollama, or a mock provider.

The most important design decision is separating intelligence from execution. The model reasons, but tools are narrow, explicit, and safe. This prevents the system from becoming an uncontrolled automation bot.

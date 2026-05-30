# MCP Security Notes

Agentic AI systems become risky when models can invoke tools. This repo demonstrates a safer baseline.

## Threat model

| Risk | Example | Control in this repo |
|---|---|---|
| Prompt injection | User asks the agent to ignore tool policy | System prompts and deterministic tool boundaries |
| Tool poisoning | Ambiguous or malicious tool descriptions | Clear tool names, narrow schemas, explicit descriptions |
| Secrets leakage | API keys sent into model context | Environment variables are not exposed to tools |
| Over-permission | Agent can run shell commands | No shell execution tool is included |
| Unauthorized channel access | Anyone can message the agent | OpenClaw config example uses allowlists and mentions |
| Model lock-in | Only one model works | Claude/Ollama/mock provider abstraction |

## Safe defaults

- MCP tools only return structured planning and review output.
- Tools do not mutate production systems.
- API adapter supports an optional header key.
- The mock provider enables safe demos without external calls.

## Production hardening checklist

- [ ] Add authentication and identity propagation between gateway and API.
- [ ] Log tool calls without logging secrets or full private prompts.
- [ ] Add per-user/session authorization.
- [ ] Add rate limits.
- [ ] Version MCP tool schemas.
- [ ] Require human approval for external actions.
- [ ] Add red-team prompts to CI.
- [ ] Store audit logs for tool invocations.

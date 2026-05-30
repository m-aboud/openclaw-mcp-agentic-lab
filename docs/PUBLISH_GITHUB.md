# Publish to GitHub

## Option A — GitHub CLI

```bash
cd openclaw-mcp-agentic-lab
git init
git add .
git commit -m "Initial OpenClaw MCP agentic AI lab"
gh repo create openclaw-mcp-agentic-lab --public --source=. --remote=origin --push
```

## Option B — Existing empty GitHub repo

```bash
cd openclaw-mcp-agentic-lab
git init
git add .
git commit -m "Initial OpenClaw MCP agentic AI lab"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/openclaw-mcp-agentic-lab.git
git push -u origin main
```

## Recommended GitHub settings

Add these repository topics:

```text
openclaw mcp model-context-protocol claude ollama multi-agent-agents agentic-ai qwen llama mistral deepseek fastapi ai-infrastructure
```

Upload `assets/social-preview.svg` or export it to PNG for the repository social preview.

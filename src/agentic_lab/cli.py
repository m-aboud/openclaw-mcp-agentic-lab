from __future__ import annotations

import json
from dataclasses import asdict

import typer
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

from .agents import MultiAgentOrchestrator
from .models import build_provider
from .tools import create_openclaw_agent_prompt, generate_repo_blueprint

load_dotenv()
app = typer.Typer(help="OpenClaw + MCP + Claude/Ollama multi-agent AI lab")
console = Console()

DEFAULT_TASK = (
    "Build a multi-agent assistant that receives tasks through OpenClaw, "
    "uses MCP tools for repository planning and security review, and can switch "
    "between Claude and local OSS models."
)


@app.command()
def run_demo(
    provider: str = typer.Option("mock", help="mock, claude, or ollama"),
    model: str | None = typer.Option(None, help="Model name, e.g. claude-opus-4-8 or qwen2.5:7b"),
    task: str = typer.Option(DEFAULT_TASK, help="Task to send through the agentic workflow"),
) -> None:
    """Run the full multi-agent demo."""
    llm = build_provider(provider=provider, model=model)
    result = MultiAgentOrchestrator(llm).run(task)
    console.print(Panel(result.final_answer, title=f"Agentic Lab — {result.provider}/{result.model}"))
    console.print_json(json.dumps(asdict(result), indent=2))


@app.command()
def blueprint(goal: str = typer.Argument(DEFAULT_TASK)) -> None:
    """Print a repo blueprint without calling an LLM."""
    console.print_json(json.dumps(generate_repo_blueprint(goal), indent=2))


@app.command("openclaw-prompt")
def openclaw_prompt() -> None:
    """Print an OpenClaw-facing agent profile."""
    prompt = create_openclaw_agent_prompt(
        role="Agentic AI platform engineer",
        context="Portfolio demo for OpenClaw, MCP, Claude, and OSS model orchestration.",
    )
    console.print_json(json.dumps(prompt, indent=2))


@app.command("mcp-server")
def mcp_server() -> None:
    """Start the MCP server over stdio."""
    from .mcp_server import mcp

    mcp.run()


if __name__ == "__main__":
    app()

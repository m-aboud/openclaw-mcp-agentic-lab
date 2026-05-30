from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .tools import (
    analyze_agent_request as analyze_agent_request_tool,
)
from .tools import (
    create_openclaw_agent_prompt as create_openclaw_agent_prompt_tool,
)
from .tools import (
    generate_repo_blueprint as generate_repo_blueprint_tool,
)
from .tools import (
    security_review as security_review_tool,
)

mcp = FastMCP("openclaw-mcp-agentic-lab")


@mcp.tool()
def analyze_agent_request(request: str) -> dict:
    """Classify an agentic AI request and extract required capabilities."""
    return analyze_agent_request_tool(request)


@mcp.tool()
def generate_repo_blueprint(goal: str, model_stack: str = "Claude + Ollama", channel: str = "OpenClaw") -> dict:
    """Generate a GitHub-ready blueprint for an agentic AI showcase repository."""
    return generate_repo_blueprint_tool(goal=goal, model_stack=model_stack, channel=channel)


@mcp.tool()
def security_review(architecture_text: str) -> dict:
    """Review an MCP/agentic architecture for practical security risks and mitigations."""
    return security_review_tool(architecture_text)


@mcp.tool()
def create_openclaw_agent_prompt(role: str, context: str) -> dict:
    """Create an OpenClaw-facing agent operating profile and system prompt."""
    return create_openclaw_agent_prompt_tool(role=role, context=context)


@mcp.resource("agentic-lab://about")
def about() -> str:
    return (
        "OpenClaw MCP Agentic Lab exposes portfolio-grade tools for building "
        "multi-agent AI workflows using Claude, Ollama/OSS models, and MCP."
    )


@mcp.prompt()
def portfolio_demo_prompt() -> str:
    return (
        "Build a multi-agent AI assistant that receives tasks through OpenClaw, "
        "uses MCP tools for repo planning and security review, and can switch between "
        "Claude and local OSS models."
    )


if __name__ == "__main__":
    mcp.run()

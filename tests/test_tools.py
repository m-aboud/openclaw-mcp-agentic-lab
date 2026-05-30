from agentic_lab.tools import analyze_agent_request, generate_repo_blueprint, security_review


def test_analyze_agent_request_detects_capabilities():
    result = analyze_agent_request("Build OpenClaw MCP agents with Claude and Ollama")
    assert result["complexity"] == "high"
    assert "openclaw" in result["capabilities_detected"]
    assert "mcp" in result["capabilities_detected"]
    assert "claude" in result["capabilities_detected"]
    assert "ollama" in result["capabilities_detected"]


def test_generate_repo_blueprint_has_core_components():
    result = generate_repo_blueprint("showcase agentic ai")
    assert result["name"] == "openclaw-mcp-agentic-lab"
    assert any("MCP" in item for item in result["components"])
    assert "src/agentic_lab" in result["folders"]


def test_security_review_adds_mcp_and_openclaw_risks():
    result = security_review("OpenClaw gateway with MCP tools")
    risk_names = [item["risk"] for item in result["risks"]]
    assert any("Messaging-channel" in risk for risk in risk_names)
    assert any("Tool poisoning" in risk for risk in risk_names)

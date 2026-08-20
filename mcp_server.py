from mcp.server import MCPServer
from wazuh_client import WazuhClient

# =========================================================
# AI-SOC MCP SERVER
# MCP 2.0
# =========================================================

mcp = MCPServer("AI-SOC Wazuh")

client = WazuhClient()


@mcp.tool()
def get_recent_alerts(limit: int = 10) -> dict:
    """Retrieve the most recent Wazuh security alerts."""
    return client.get_recent_alerts(limit=limit)


@mcp.tool()
def search_alerts(query: str, limit: int = 20) -> dict:
    """Search Wazuh alerts using a security-related query."""
    return client.search_alerts(
        query=query,
        limit=limit
    )


@mcp.tool()
def get_alert_summary() -> dict:
    """Get Wazuh alert severity statistics."""
    return client.get_alert_summary()


@mcp.tool()
def check_wazuh_health() -> dict:
    """Check Wazuh Indexer health through the Alert Bridge."""
    return client.health()


if __name__ == "__main__":

    print("=" * 70)
    print("                 AI-SOC MCP SERVER")
    print("=" * 70)

    print()
    print("Available Wazuh tools:")
    print("  • get_recent_alerts")
    print("  • search_alerts")
    print("  • get_alert_summary")
    print("  • check_wazuh_health")
    print()

    print("Starting MCP server...")

    mcp.run()
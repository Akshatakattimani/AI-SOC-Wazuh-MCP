import os
import requests
from dotenv import load_dotenv

# =========================================================
# AI-SOC WAZUH CLIENT
# Windows → Kali Alert Bridge → Wazuh Indexer
# =========================================================

load_dotenv()

BRIDGE_URL = os.getenv(
    "WAZUH_BRIDGE_URL",
    "http://192.168.56.102:5600"
)


class WazuhClient:

    def __init__(self):
        self.base_url = BRIDGE_URL.rstrip("/")

    # -----------------------------------------------------
    # Generic GET
    # -----------------------------------------------------

    def get(self, endpoint, params=None):

        url = f"{self.base_url}{endpoint}"

        response = requests.get(
            url,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    # -----------------------------------------------------
    # Bridge health
    # -----------------------------------------------------

    def health(self):

        return self.get("/health")

    # -----------------------------------------------------
    # Recent alerts
    # -----------------------------------------------------

    def get_recent_alerts(self, limit=10):

        return self.get(
            "/alerts/recent",
            params={
                "limit": limit
            }
        )

    # -----------------------------------------------------
    # Search alerts
    # -----------------------------------------------------

    def search_alerts(
        self,
        query,
        limit=20
    ):

        return self.get(
            "/alerts/search",
            params={
                "q": query,
                "limit": limit
            }
        )

    # -----------------------------------------------------
    # Alert summary
    # -----------------------------------------------------

    def get_alert_summary(self):

        return self.get(
            "/alerts/summary"
        )


# =========================================================
# DISPLAY HELPERS
# =========================================================

def display_alert(alert, number):

    rule = alert.get(
        "rule",
        {}
    )

    agent = alert.get(
        "agent",
        {}
    )

    print()
    print("-" * 70)

    print(
        f"Alert #{number}"
    )

    print(
        f"  Alert ID    : "
        f"{alert.get('id', 'N/A')}"
    )

    print(
        f"  Agent       : "
        f"{agent.get('name', 'N/A')}"
    )

    print(
        f"  Agent ID    : "
        f"{agent.get('id', 'N/A')}"
    )

    print(
        f"  Rule ID     : "
        f"{rule.get('id', 'N/A')}"
    )

    print(
        f"  Severity    : "
        f"{rule.get('level', 'N/A')}"
    )

    print(
        f"  Description : "
        f"{rule.get('description', 'N/A')}"
    )

    print(
        f"  Timestamp   : "
        f"{alert.get('timestamp', 'N/A')}"
    )

    print(
        f"  Location    : "
        f"{alert.get('location', 'N/A')}"
    )

    groups = rule.get(
        "groups",
        []
    )

    if groups:

        print(
            f"  Groups      : "
            f"{', '.join(groups)}"
        )

    mitre = rule.get(
        "mitre",
        {}
    )

    if mitre:

        techniques = mitre.get(
            "technique",
            []
        )

        tactics = mitre.get(
            "tactic",
            []
        )

        if techniques:

            print(
                f"  MITRE       : "
                f"{', '.join(techniques)}"
            )

        if tactics:

            print(
                f"  Tactics     : "
                f"{', '.join(tactics)}"
            )


# =========================================================
# MAIN TEST
# =========================================================

def main():

    print("=" * 70)
    print("                    AI-SOC WAZUH CLIENT")
    print("=" * 70)

    print(
        f"\nAlert Bridge : {BRIDGE_URL}"
    )

    client = WazuhClient()

    # -----------------------------------------------------
    # Health
    # -----------------------------------------------------

    print(
        "\nChecking Alert Bridge..."
    )

    try:

        health = client.health()

        print(
            "✅ Alert Bridge is reachable."
        )

        print(
            f"Indexer status: "
            f"{health.get('indexer', {}).get('status', 'unknown')}"
        )

    except Exception as error:

        print(
            "❌ Alert Bridge connection failed."
        )

        print(
            f"Error: {error}"
        )

        return

    # -----------------------------------------------------
    # Recent alerts
    # -----------------------------------------------------

    print(
        "\nRetrieving recent Wazuh alerts..."
    )

    try:

        result = client.get_recent_alerts(
            limit=10
        )

        alerts = result.get(
            "alerts",
            []
        )

        print(
            f"✅ Alerts returned: "
            f"{len(alerts)}"
        )

    except Exception as error:

        print(
            "❌ Failed to retrieve alerts."
        )

        print(
            f"Error: {error}"
        )

        return

    # -----------------------------------------------------
    # Display alerts
    # -----------------------------------------------------

    for number, alert in enumerate(
        alerts,
        start=1
    ):

        display_alert(
            alert,
            number
        )

    # -----------------------------------------------------
    # Summary
    # -----------------------------------------------------

    print("\n")
    print("=" * 70)
    print("                       SOC SUMMARY")
    print("=" * 70)

    try:

        result = client.get_alert_summary()

        print("\n✅ Summary retrieved successfully.")

        print("\nRaw summary:")

        print(result)

    except Exception as error:

        print(
            f"\n⚠️ Summary failed: {error}"
        )

    print("\n")
    print("=" * 70)
    print("                 WAZUH CLIENT TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":

    main()
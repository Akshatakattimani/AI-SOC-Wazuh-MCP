import os
import requests
import urllib3
from dotenv import load_dotenv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

# -----------------------------
# Configuration
# -----------------------------

WAZUH_HOST = os.getenv("WAZUH_HOST")
WAZUH_PORT = os.getenv("WAZUH_PORT")
WAZUH_USER = os.getenv("WAZUH_USER")
WAZUH_PASSWORD = os.getenv("WAZUH_PASSWORD")

BASE_URL = f"https://{WAZUH_HOST}:{WAZUH_PORT}"


# -----------------------------
# Authenticate with Wazuh API
# -----------------------------

def authenticate():

    url = f"{BASE_URL}/security/user/authenticate?raw=true"

    response = requests.post(
        url,
        auth=(WAZUH_USER, WAZUH_PASSWORD),
        verify=False
    )

    response.raise_for_status()

    return response.text.strip()


# -----------------------------
# Get Wazuh API information
# -----------------------------

def get_api_info(token):

    url = f"{BASE_URL}/"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(
        url,
        headers=headers,
        verify=False
    )

    response.raise_for_status()

    return response.json()


# -----------------------------
# Get alerts from Wazuh Indexer
# -----------------------------

def get_recent_alerts():

    # Indexer is currently accessible only
    # from Kali localhost.
    indexer_url = "https://127.0.0.1:9200"

    index = "wazuh-alerts-4.x-*"

    url = f"{indexer_url}/{index}/_search"

    query = {
        "size": 10,
        "sort": [
            {
                "@timestamp": {
                    "order": "desc"
                }
            }
        ],
        "_source": [
            "timestamp",
            "@timestamp",
            "agent",
            "manager",
            "rule",
            "decoder",
            "data",
            "full_log",
            "location"
        ]
    }

    # IMPORTANT:
    # These credentials are NOT the Wazuh API credentials.
    # They are the Wazuh Indexer credentials.
    indexer_user = os.getenv("INDEXER_USER")
    indexer_password = os.getenv("INDEXER_PASSWORD")

    response = requests.get(
        url,
        auth=(indexer_user, indexer_password),
        json=query,
        verify=False
    )

    response.raise_for_status()

    return response.json()


# -----------------------------
# Display alerts like a SOC analyst
# -----------------------------

def display_alerts(result):

    hits = result.get("hits", {}).get("hits", [])

    if not hits:
        print("\nNo Wazuh alerts found.")
        return

    print("\n")
    print("=" * 70)
    print("                 WAZUH SOC ALERTS")
    print("=" * 70)

    print(f"\nTotal alerts returned: {len(hits)}")

    for number, hit in enumerate(hits, start=1):

        alert = hit.get("_source", {})

        agent = alert.get("agent", {})
        rule = alert.get("rule", {})
        decoder = alert.get("decoder", {})
        data = alert.get("data", {})

        print("\n" + "-" * 70)

        print(f"Alert #{number}")

        print(f"Agent        : {agent.get('name', 'N/A')}")
        print(f"Agent ID     : {agent.get('id', 'N/A')}")

        print(f"Rule ID      : {rule.get('id', 'N/A')}")
        print(f"Severity     : {rule.get('level', 'N/A')}")

        print(
            f"Description  : "
            f"{rule.get('description', 'N/A')}"
        )

        print(
            f"Decoder      : "
            f"{decoder.get('name', 'N/A')}"
        )

        print(
            f"Timestamp    : "
            f"{alert.get('timestamp', alert.get('@timestamp', 'N/A'))}"
        )

        print(
            f"Location     : "
            f"{alert.get('location', 'N/A')}"
        )

        if data:
            print(f"Data         : {data}")

        print(
            f"Full Log     : "
            f"{alert.get('full_log', 'N/A')}"
        )

    print("\n" + "=" * 70)


# -----------------------------
# Main
# -----------------------------

def main():

    print("=" * 70)
    print("              AI-SOC WAZUH CLIENT")
    print("=" * 70)

    try:

        # Step 1
        print("\n[1] Authenticating with Wazuh API...")

        token = authenticate()

        print("    Authentication successful.")
        print("    JWT received.")

        # Step 2
        print("\n[2] Testing Wazuh API...")

        api_info = get_api_info(token)

        api_data = api_info.get("data", {})

        print(
            f"    Wazuh API version: "
            f"{api_data.get('api_version', 'N/A')}"
        )

        # Step 3
        print("\n[3] Querying Wazuh Indexer...")

        result = get_recent_alerts()

        print("    Alerts retrieved successfully.")

        # Step 4
        print("\n[4] Formatting alerts for SOC analyst...")

        display_alerts(result)

    except requests.exceptions.ConnectionError as error:

        print("\n❌ Connection error.")
        print(error)

    except requests.exceptions.HTTPError as error:

        print("\n❌ HTTP error.")
        print(error)

    except Exception as error:

        print("\n❌ Unexpected error.")
        print(error)


if __name__ == "__main__":
    main()
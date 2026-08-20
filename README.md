\# AI-Powered SOC Assistant — Wazuh + MCP



> \*\*Project Status:\*\* 🚧 In Development



An AI-assisted Security Operations Center (SOC) project that integrates \*\*Wazuh security monitoring\*\* with the \*\*Model Context Protocol (MCP)\*\* to expose real security alerts and investigation capabilities to an AI layer.



\## 🎯 Project Objective



The goal of this project is to build a SOC assistant capable of helping analysts investigate security events using real-time Wazuh telemetry.



The project is being developed in stages:



1\. Wazuh security monitoring

2\. Python-based Wazuh integration

3\. MCP server and security investigation tools

4\. Local AI integration using Ollama

5\. AI-assisted alert investigation

6\. SOC analyst question-and-answer workflow



## 🏗️ Current Architecture

The current system follows this workflow:

1. **Windows Host**
   - Wazuh Agent collects security telemetry.

2. **Kali Linux**
   - Wazuh Manager receives and processes events.
   - Wazuh Indexer stores security events.
   - Wazuh Dashboard provides monitoring and investigation.

3. **Python Alert Bridge**
   - Runs on port `5600`.
   - Provides access to Wazuh alert data.

4. **Python Wazuh Client**
   - Connects to the Alert Bridge.
   - Retrieves recent Wazuh alerts and SOC summary information.

5. **MCP Server**
   - Exposes Wazuh investigation capabilities as MCP tools.

6. **MCP Inspector**
   - Used to test and interact with the MCP tools.

&#x20;            |

&#x20;            v

&#x20;       MCP Inspector


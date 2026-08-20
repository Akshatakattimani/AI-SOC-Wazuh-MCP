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



\## 🏗️ Current Architecture



```text

Windows Host

&#x20;    │

&#x20;    │ Wazuh Agent

&#x20;    ▼

Kali Linux

&#x20;    │

&#x20;    ├── Wazuh Manager

&#x20;    ├── Wazuh Indexer

&#x20;    └── Wazuh Dashboard

&#x20;            │

&#x20;            ▼

&#x20;      Python Alert Bridge

&#x20;         Port 5600

&#x20;            │

&#x20;            ▼

&#x20;       Python Wazuh Client

&#x20;            │

&#x20;            ▼

&#x20;         MCP Server

&#x20;            │

&#x20;            ▼

&#x20;       MCP Inspector





\## 🛠️ Current Implementation



The current implementation successfully connects Wazuh security monitoring with a custom MCP server and retrieves real Wazuh security alerts through MCP tools.



\### Available MCP Tools



\- `get\_recent\_alerts`

\- `search\_alerts`

\- `get\_alert\_summary`

\- `check\_wazuh\_health`


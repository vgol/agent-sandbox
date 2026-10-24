# Marusya Agent Harness

<a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.14-3776AB?logo=python&amp;logoColor=white" alt="Python 3.14"></a>
<a href="https://openai.com/codex/"><img src="https://img.shields.io/badge/OpenAI%20Codex-AI%20coding-412991?logo=openai&amp;logoColor=white" alt="OpenAI Codex — AI coding"></a>
<a href="https://github.com/features/copilot"><img src="https://img.shields.io/badge/GitHub%20Copilot-AI%20coding-000000?logo=githubcopilot&amp;logoColor=white" alt="GitHub Copilot — AI coding"></a>
<a href="https://github.com/NousResearch/hermes-agent"><img src="https://img.shields.io/badge/Hermes%20Agent-Automation-FFD700" alt="Hermes Agent — Automation"></a>

Marusya Agent Harness is a workspace for automations powered by
[Hermes Agent](https://github.com/NousResearch/hermes-agent), covering:

- Coding and software development
- Finance and accounting
- Document and email processing

This repository will hold the non-private code, configurations, and workflows
related to the agent's work. Private data and credentials stay outside the project.

## Getting started

Open this repository in GitHub Codespaces, or open it locally in Visual Studio Code
with Docker and the Dev Containers extension installed. In VS Code, run
**Dev Containers: Reopen in Container** to build and enter the development environment.

The environment is configured in [`.devcontainer/devcontainer.json`](.devcontainer/devcontainer.json)
and uses a Debian Bookworm-based development container.

## Included tools

The development container is configured to install:

- Zsh with Oh My Zsh
- Docker-in-Docker
- GitHub Copilot CLI
- GitHub CLI
- Dev Container CLI
- TypeScript
- uv for Python package and project management

Authenticate the GitHub tools as needed before using features that require an account.
Keep credentials and API keys out of the repository.

## License

This project is licensed under the [Apache License 2.0](LICENSE).

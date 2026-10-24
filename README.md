# agent-sandbox

A sandbox for trying out popular agentic harnesses and AI-assisted development workflows.

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

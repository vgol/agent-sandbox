# Marusya Agent

Marusya Agent is a workspace for AI-assisted automation powered by
[Hermes Agent](https://github.com/NousResearch/hermes-agent). Its intended use
cases include:

- Coding and software development
- Finance and accounting
- Document and email processing

This repository holds the non-private code, infrastructure configuration and
development tooling for the project. Private documents, credentials and agent
session data should stay outside version control.

## Current scope

The repository currently provides a development container and Terraform
configuration for an OVHcloud VPS. The VPS configuration is preparation only:
it does not represent an already provisioned agent deployment, and purchasing
is blocked by default.

## Getting started

Open the repository in GitHub Codespaces, or locally in Visual Studio Code
with Docker and the Dev Containers extension installed. Run
**Dev Containers: Rebuild and Reopen in Container** to build and enter the
development environment.

The environment is configured in
[`.devcontainer/devcontainer.json`](.devcontainer/devcontainer.json) and uses
a Debian Bookworm base with:

- Zsh and Oh My Zsh
- Docker-in-Docker
- GitHub Copilot CLI and GitHub CLI
- Dev Container CLI
- TypeScript
- uv and uvx for Python tooling
- Terraform CLI and the HashiCorp Terraform VS Code extension

The [devcontainer Dockerfile](.devcontainer/Dockerfile) installs uv and uvx
from Astral's official image. Authenticate individual tools only when needed;
do not commit authentication tokens.

To build and enter the environment through the Dev Container CLI:

```sh
devcontainer up --workspace-folder .
devcontainer exec --workspace-folder . bash
```

These commands require Docker and the Dev Container CLI on the host.

## OVHcloud infrastructure

The [VPS setup guide](infra/ovh-vps/README.md) documents the selected VPS-1
plan, Ubuntu installation, location preferences, pricing checks and credential
setup. Europe is preferred, with Canada as a fallback when European stock is
unavailable. Recheck availability and the account-specific checkout price
before approving any purchase.

Validate the configuration from the repository root without ordering a VPS:

```sh
terraform -chdir=infra/ovh-vps init -backend=false
terraform -chdir=infra/ovh-vps fmt -check
terraform -chdir=infra/ovh-vps validate
```

Do not run an order-capable `terraform apply` until its cost and plan have
been explicitly approved.

## Local files and secrets

The root [`.gitignore`](.gitignore) covers local environments, Terraform
provider downloads, state, saved plans, variable files and OVH configuration.
Keep dependency lockfiles in version control. Ignore rules are not a security
boundary: review changes for secrets before committing, and protect local
Terraform state and plan files.

## License

Licensed under the [Apache License 2.0](LICENSE).

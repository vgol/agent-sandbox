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
configuration that adopts a manually ordered OVHcloud VPS by import. The
configuration never orders servers, and no agent deployment exists yet.

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
- OVHcloud CLI

For an existing Codespace that reports Terraform missing, run
**Codespaces: Rebuild Container** to pick up the configured feature, then
check `terraform version` in a new terminal.

The [devcontainer Dockerfile](.devcontainer/Dockerfile) installs uv and uvx
from Astral's official image and the OVHcloud CLI from OVHcloud's official
image. Authenticate individual tools only when needed; do not commit
authentication tokens.

To build and enter the environment through the Dev Container CLI:

```sh
devcontainer up --workspace-folder .
devcontainer exec --workspace-folder . bash
```

These commands require Docker and the Dev Container CLI on the host.

## OVHcloud infrastructure

The [VPS setup guide](infra/ovh-vps/README.md) explains how the manually
ordered VPS-1 is imported into Terraform, how to find its service name and how
to supply read-only API credentials.

Validate the configuration from the repository root:

```sh
terraform -chdir=infra/ovh-vps init -backend=false
terraform -chdir=infra/ovh-vps fmt -check
terraform -chdir=infra/ovh-vps validate
```

Review the first `terraform plan`: it must show the import, optionally an
in-place display-name update to `marusya-agent`, and no
create, replace or destroy.

## Local files and secrets

The root [`.gitignore`](.gitignore) covers local environments, Terraform
provider downloads, state, saved plans, variable files and OVH configuration.
Keep dependency lockfiles in version control. Ignore rules are not a security
boundary: review changes for secrets before committing, and protect local
Terraform state and plan files.

## License

Licensed under the [Apache License 2.0](LICENSE).

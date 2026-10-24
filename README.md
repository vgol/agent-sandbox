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

## Hermes Docker image

The image extends the [official Hermes Agent image](https://hermes-agent.nousresearch.com/docs/user-guide/docker)
and copies this repository into `/workspace`, the agent's terminal working directory.
Hermes itself stays in `/opt/hermes`; configuration and sessions persist in
`/opt/data`. The official entrypoint and process supervision are preserved.
The base image is pinned to the `v0.22.5` release tag rather than `latest`.
Release tags can be reassigned upstream; use an image digest if strict
reproducibility is required. To upgrade, update `HERMES_IMAGE` in `Dockerfile`
and run the smoke test below.

### Build and configure

```sh
docker build -t agent-sandbox-hermes:local .
export API_SERVER_KEY="$(openssl rand -hex 32)"
docker compose run --rm hermes setup
docker compose up -d --build
```

The one-time setup configures a model provider and stores its credentials in the
named `hermes-data` volume. Keep `API_SERVER_KEY` in your shell or a local `.env`
file for subsequent Compose commands. Never commit credentials. Local `.env`
files, Git metadata, virtual environments, and private key files are excluded
from the build context.

### Interact from the devcontainer

Run these commands from the repository root in the VS Code terminal. With
Docker-in-Docker, the published API is reachable from the devcontainer at
`http://127.0.0.1:8642`; no Codespaces port forwarding is needed for this access.

For an already running service, configure a model provider interactively, then
restart the gateway so it loads the new configuration:

```sh
docker compose exec hermes hermes setup
docker compose restart hermes
```

Start an interactive terminal chat or send a single prompt:

```sh
docker compose exec hermes hermes chat
docker compose exec hermes hermes chat --oneshot -q "Summarize this repository"
```

These CLI commands start separate agent sessions; they do not attach to an
existing API conversation. To call the running gateway API, load the API key
from your local `.env` file first:

```sh
set -a
. ./.env
set +a
curl --fail http://127.0.0.1:8642/v1/chat/completions \
  -H "Authorization: Bearer $API_SERVER_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"hermes-agent","messages":[{"role":"user","content":"Summarize this repository"}]}'
```

The repository is copied into the image, not bind-mounted. Agent edits stay in
the container and do not update the devcontainer checkout. Rebuild with
`docker compose up -d --build` to include host-side source changes; this also
replaces the container, discarding edits outside the persisted data volume.
Use `docker compose ps` for status and `docker compose logs --tail=100 hermes`
for gateway logs.

### Reach the agent

The [Hermes API server](https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server)
listens on `0.0.0.0:8642` inside the container. Compose publishes it only to host
loopback by default. A random `API_SERVER_KEY` is required; no key is baked into
the image.

```sh
curl --fail http://127.0.0.1:8642/health
curl --fail http://127.0.0.1:8642/v1/models \
  -H "Authorization: Bearer $API_SERVER_KEY"
curl --fail http://127.0.0.1:8642/v1/chat/completions \
  -H "Authorization: Bearer $API_SERVER_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"hermes-agent","messages":[{"role":"user","content":"Hello!"}]}'
```

For access from another machine, set `HERMES_BIND_ADDRESS=0.0.0.0` before
starting Compose, and use a firewall and an HTTPS reverse proxy. Treat the API
as privileged access to an agent with terminal and file tools. The health
endpoint is public; agent API requests require a bearer token. Override the
host port with `HERMES_PORT` if necessary.

For a plain Docker launch after building:

```sh
docker run --rm -p 127.0.0.1:8642:8642 \
  -e API_SERVER_KEY -v hermes-data:/opt/data \
  agent-sandbox-hermes:local
```

Plain Docker's `hermes-data` volume is separate from Compose's project-prefixed
volume. Configure it once with:

```sh
docker run --rm -it -v hermes-data:/opt/data agent-sandbox-hermes:local setup
```

### Smoke test

Requires Python 3 and Docker, but no model-provider credentials:

```sh
python3 tests/smoke.py
```

If the host Python installation is incomplete, use a complete runtime with
`uv run --no-project --python 3.12 python tests/smoke.py`.

This builds the image, launches the real Hermes gateway and a local mock
OpenAI-compatible model provider, and checks host-side health, authentication,
copied source, and an end-to-end agent completion. Test containers, their data
volumes, and the temporary network are removed even on failure. The built image
remains available as `agent-sandbox-hermes:smoke`. This tests the agent integration,
not connectivity to a live external model provider.

Stop the deployment with `docker compose down`. Configuration survives this;
`docker compose down --volumes` also deletes the persisted agent data.

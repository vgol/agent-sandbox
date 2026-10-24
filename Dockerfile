ARG HERMES_IMAGE=nousresearch/hermes-agent:v0.22.5
FROM ${HERMES_IMAGE}

WORKDIR /workspace
COPY --chown=hermes:hermes . .

ENV API_SERVER_ENABLED=true \
    API_SERVER_HOST=0.0.0.0 \
    API_SERVER_PORT=8642 \
    TERMINAL_CWD=/workspace

EXPOSE 8642

HEALTHCHECK --interval=30s --timeout=5s --start-period=120s --retries=3 \
    CMD ["python", "-c", "import json, urllib.request; r = json.load(urllib.request.urlopen('http://127.0.0.1:8642/health', timeout=3)); assert r['status'] == 'ok' and r['platform'] == 'hermes-agent'"]

CMD ["gateway", "run"]

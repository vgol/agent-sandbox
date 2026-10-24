"""Build and exercise the real Hermes gateway against a local mock LLM."""

import argparse
import json
import secrets
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from http.client import RemoteDisconnected


REPLY = "Hermes container smoke test passed."


class MockProvider(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/v1/models":
            self.send_error(404)
            return
        self.respond({"object": "list", "data": [
            {"id": "hermes-smoke", "object": "model", "owned_by": "smoke-test"}
        ]})

    def respond(self, body):
        encoded = json.dumps(body).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_POST(self):
        if self.path != "/v1/chat/completions":
            self.send_error(404)
            return
        request = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        body = {
            "id": "chatcmpl-smoke",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": "hermes-smoke",
            "choices": [{"index": 0, "message": {
                "role": "assistant", "content": REPLY
            }, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 10, "completion_tokens": 8, "total_tokens": 18},
        }
        if request.get("stream"):
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.end_headers()
            body["object"] = "chat.completion.chunk"
            body["choices"][0]["delta"] = body["choices"][0].pop("message")
            self.wfile.write(
                f"data: {json.dumps(body)}\n\ndata: [DONE]\n\n".encode()
            )
        else:
            self.respond(body)


def docker(*args):
    return subprocess.check_output(["docker", *args], text=True).strip()


def smoke(image):
    suffix = uuid.uuid4().hex[:12]
    network = f"hermes-smoke-{suffix}"
    provider = f"{network}-provider"
    gateway = f"{network}-gateway"
    key = secrets.token_hex(32)
    docker("build", "--tag", image, ".")
    docker("network", "create", network)
    try:
        docker(
            "run", "--detach", "--name", provider, "--network", network,
            "--entrypoint", "python", image,
            "/workspace/tests/smoke.py", "--mock-provider",
        )
        docker(
            "create", "--name", gateway, "--network", network,
            "--publish", "127.0.0.1::8642",
            "--env", f"API_SERVER_KEY={key}",
            "--env", "HERMES_INFERENCE_PROVIDER=custom",
            "--env", f"OPENAI_BASE_URL=http://{provider}:8000/v1",
            "--env", "OPENAI_API_KEY=smoke-test-not-a-real-provider-key",
            image,
        )
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json") as config:
            json.dump({"model": {
                "default": "hermes-smoke",
                "provider": "custom",
                "base_url": f"http://{provider}:8000/v1",
                "api_mode": "chat_completions",
            }}, config)
            config.flush()
            docker("cp", config.name, f"{gateway}:/opt/data/config.yaml")
        docker("start", gateway)
        bindings = json.loads(docker("inspect", gateway))[0]["NetworkSettings"]["Ports"]
        url = f"http://127.0.0.1:{bindings['8642/tcp'][0]['HostPort']}"
        deadline = time.monotonic() + 180
        while True:
            try:
                with urllib.request.urlopen(f"{url}/health", timeout=3) as response:
                    health = json.load(response)
                assert health["status"] == "ok", health
                assert health["platform"] == "hermes-agent", health
                break
            except (urllib.error.URLError, TimeoutError, ConnectionError, RemoteDisconnected):
                if time.monotonic() >= deadline:
                    raise TimeoutError("Hermes gateway did not become reachable")
                time.sleep(2)
        print(f"PASS: gateway reachable from host at {url}", flush=True)
        try:
            urllib.request.urlopen(f"{url}/v1/models", timeout=5)
        except urllib.error.HTTPError as error:
            assert error.code == 401, error.code
        else:
            raise AssertionError("Unauthenticated model request was accepted")
        request = urllib.request.Request(
            f"{url}/v1/models", headers={"Authorization": f"Bearer {key}"}
        )
        with urllib.request.urlopen(request, timeout=10) as response:
            models = json.load(response)
        assert models["object"] == "list" and models["data"], models
        print("PASS: API rejects unauthenticated calls and accepts bearer token", flush=True)
        docker("exec", gateway, "test", "-f", "/workspace/README.md")
        docker("exec", gateway, "test", "!", "-e", "/workspace/.git")
        docker("exec", gateway, "test", "!", "-e", "/workspace/.env")
        print("PASS: project copied without Git metadata or local .env", flush=True)
        request = urllib.request.Request(
            f"{url}/v1/chat/completions",
            data=json.dumps({
                "model": "hermes-smoke",
                "messages": [{"role": "user", "content": "Say the smoke test result."}],
                "stream": False,
            }).encode(),
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        )
        with urllib.request.urlopen(request, timeout=120) as response:
            completion = json.load(response)
        assert completion["choices"][0]["message"]["content"] == REPLY, completion
        assert completion["choices"][0]["finish_reason"] == "stop", completion
        print("PASS: real Hermes agent returned the local mock provider response", flush=True)
        docker("exec", gateway, "python", "-c",
               "import json, urllib.request; "
               "r = json.load(urllib.request.urlopen('http://127.0.0.1:8642/health')); "
               "assert r['status'] == 'ok' and r['platform'] == 'hermes-agent'")
        deadline = time.monotonic() + 60
        while True:
            health = json.loads(docker("inspect", gateway))[0]["State"]["Health"]
            if health["Status"] == "healthy":
                break
            if health["Status"] == "unhealthy" or time.monotonic() >= deadline:
                raise AssertionError(f"Container did not become healthy: {health}")
            time.sleep(2)
        print("PASS: Docker reports container healthy", flush=True)
    except Exception:
        for name in (gateway, provider):
            subprocess.run(["docker", "logs", "--tail", "80", name], check=False)
        raise
    finally:
        for name in (gateway, provider):
            subprocess.run(["docker", "rm", "--force", "--volumes", name], check=False)
        subprocess.run(["docker", "network", "rm", network], check=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mock-provider", action="store_true")
    parser.add_argument("--image", default="agent-sandbox-hermes:smoke")
    args = parser.parse_args()
    if args.mock_provider:
        ThreadingHTTPServer(("0.0.0.0", 8000), MockProvider).serve_forever()
    else:
        smoke(args.image)

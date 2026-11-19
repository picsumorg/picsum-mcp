#!/usr/bin/env python3
"""Validate local MCP client examples. Does not contact the network."""

from __future__ import annotations

import json
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENDPOINT = "https://picsum.org/mcp"

JSON_FILES = {
    ROOT / "gemini-extension.json": "gemini-extension",
    ROOT / "clients" / "claude-code.mcp.json": "claude-code",
    ROOT / "clients" / "cursor.mcp.json": "cursor",
    ROOT / "clients" / "vscode.mcp.json": "vscode",
    ROOT / "clients" / "gemini.mcpServers.json": "gemini-settings",
}

FORBIDDEN_KEYS = {
    "client_secret",
    "clientsecret",
    "client_id",
    "clientid",
    "access_token",
    "refresh_token",
    "api_key",
    "apikey",
    "authorization",
    "bearer_token_env_var",
    "headers",
    "auth",
    "oauthclientid",
    "trust",
}

errors: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def walk_keys(value: object, location: str) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key.lower().replace("-", "_") in FORBIDDEN_KEYS or key.lower() in {
                "client_secret",
                "clientsecret",
            }:
                fail(f"{location}: forbidden key {key!r}")
            walk_keys(child, f"{location}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            walk_keys(child, f"{location}[{index}]")
    elif isinstance(value, str):
        lowered = value.lower()
        if "bearer " in lowered or "sk_live" in lowered or "client_secret" in lowered:
            fail(f"{location}: forbidden credential-like string")


def require_url(entry: object, location: str) -> dict:
    if not isinstance(entry, dict):
        fail(f"{location}: server entry must be an object")
        return {}
    if entry.get("url") != ENDPOINT:
        fail(f"{location}: url must be {ENDPOINT}")
    if "httpUrl" in entry or "command" in entry or "args" in entry:
        fail(f"{location}: local or deprecated transport fields are not allowed")
    walk_keys(entry, location)
    return entry


def main() -> int:
    loaded: dict[str, object] = {}
    for path, label in JSON_FILES.items():
        try:
            loaded[label] = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001 - report the parser error and continue
            fail(f"{path.relative_to(ROOT)}: invalid JSON ({exc})")

    extension = loaded.get("gemini-extension")
    if isinstance(extension, dict):
        name = extension.get("name")
        version = extension.get("version")
        if name != "picsum-mcp":
            fail("gemini-extension.json: name must be picsum-mcp")
        elif not isinstance(name, str) or not all(
            character.islower() or character.isdigit() or character == "-"
            for character in name
        ):
            fail("gemini-extension.json: name must use lowercase letters, digits, and dashes")
        if version != "1.0.0":
            fail("gemini-extension.json: version must be 1.0.0")
        if not isinstance(extension.get("description"), str) or not extension["description"].strip():
            fail("gemini-extension.json: description is required")
        if extension.get("contextFileName") != "GEMINI.md":
            fail("gemini-extension.json: contextFileName must be GEMINI.md")
        servers = extension.get("mcpServers")
        if not isinstance(servers, dict) or set(servers) != {"picsum"}:
            fail("gemini-extension.json: mcpServers must contain only picsum")
        else:
            entry = require_url(servers["picsum"], "gemini-extension.json picsum")
            if entry.get("type") != "http":
                fail("gemini-extension.json: type must be http")
            oauth = entry.get("oauth")
            if oauth != {"enabled": True}:
                fail("gemini-extension.json: oauth must be exactly {enabled: true}")
    elif "gemini-extension" in loaded:
        fail("gemini-extension.json: document must be an object")

    for label, filename, require_type, require_tools in (
        ("claude-code", "clients/claude-code.mcp.json", True, False),
        ("cursor", "clients/cursor.mcp.json", False, False),
        ("vscode", "clients/vscode.mcp.json", True, True),
        ("gemini-settings", "clients/gemini.mcpServers.json", True, False),
    ):
        document = loaded.get(label)
        if not isinstance(document, dict):
            continue
        servers = document.get("mcpServers")
        if not isinstance(servers, dict) or set(servers) != {"picsum"}:
            fail(f"{filename}: mcpServers must contain only picsum")
            continue
        entry = require_url(servers["picsum"], f"{filename} picsum")
        if require_type and entry.get("type") != "http":
            fail(f"{filename}: type must be http")
        if not require_type and "type" in entry:
            fail(f"{filename}: Cursor remote example must not add type")
        if require_tools and entry.get("tools") != ["*"]:
            fail(f"{filename}: tools must be [\"*\"]")
        if label == "gemini-settings" and entry.get("oauth") != {"enabled": True}:
            fail(f"{filename}: oauth must be exactly {{enabled: true}}")
        if label != "gemini-settings" and "oauth" in entry:
            fail(f"{filename}: leave OAuth fields to client discovery")

    toml_path = ROOT / "clients" / "codex.config.toml"
    try:
        codex = tomllib.loads(toml_path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        fail(f"clients/codex.config.toml: invalid TOML ({exc})")
        codex = {}
    servers = codex.get("mcp_servers") if isinstance(codex, dict) else None
    if not isinstance(servers, dict) or set(servers) != {"picsum"}:
        fail("clients/codex.config.toml: mcp_servers must contain only picsum")
    else:
        entry = servers["picsum"]
        if not isinstance(entry, dict) or entry.get("url") != ENDPOINT:
            fail("clients/codex.config.toml: url must be the hosted endpoint")
        if isinstance(entry, dict) and set(entry) != {"url"}:
            fail("clients/codex.config.toml: only url is allowed")

    context = ROOT / "GEMINI.md"
    if not context.is_file() or "https://picsum.org/mcp" not in context.read_text(encoding="utf-8"):
        fail("GEMINI.md: missing hosted endpoint")

    if errors:
        for message in errors:
            print(f"error: {message}", file=sys.stderr)
        print(f"{len(errors)} error(s)", file=sys.stderr)
        return 1

    print("Validated 5 JSON documents and clients/codex.config.toml")
    print("Endpoint: https://picsum.org/mcp")
    print("Credential keys: none found")
    print("Network and OAuth: not contacted")
    return 0


if __name__ == "__main__":
    sys.exit(main())

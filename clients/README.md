# Client configuration examples

These files are copy-ready connection snippets for the hosted Lorem Picsum MCP server at `https://picsum.org/mcp`. They are examples for your own client configuration. They are not a server, a license, or a credential store.

Every example omits client IDs, client secrets, access tokens, refresh tokens, and API keys. The hosted server publishes a dynamic client registration endpoint and accepts public clients (`token_endpoint_auth_method` `none`) with PKCE `S256`. A static client secret is not part of the published connection flow on [https://picsum.org/connect](https://picsum.org/connect).

Sign-in was not run while preparing these files. After you merge a snippet into your own configuration, use that client's documented sign-in command and approve the consent page in your browser.

## claude-code.mcp.json

Shape checked against the [Claude Code MCP guide](https://code.claude.com/docs/en/mcp) and [MCP quickstart](https://code.claude.com/docs/en/mcp-quickstart). An HTTP entry needs `type` and `url`. Claude Code treats an entry that has `url` and no `type` as a local stdio server and skips it.

For one project, save this document as `.mcp.json` in the project root, or merge the `picsum` entry into the `mcpServers` object you already have. You can also register it from the shell:

```bash
claude mcp add --transport http picsum https://picsum.org/mcp
```

Then, in an interactive Claude Code session, run `/mcp`, select `picsum`, and authenticate. The same sign-in is available from the shell with `claude mcp login picsum`. Do not add an `Authorization` header. Claude Code uses a configured `Authorization` header instead of OAuth when that header is present.

Leave `oauth.scopes` unset. Claude Code then follows discovery rather than a scope list copied into this repository. The protected-resource metadata advertises `photos:read`.

## cursor.mcp.json

Shape checked against the [Cursor MCP documentation](https://cursor.com/docs/mcp). A remote server entry is a `url`. The current remote example does not use a `type` field, so this file does not add one.

Merge the `picsum` entry into `mcpServers` in either `~/.cursor/mcp.json` (all projects) or `.cursor/mcp.json` (one project). Cursor's documented OAuth path for a server that supports dynamic client registration uses the authorization-code flow with PKCE and registers a public client. The static `auth.CLIENT_ID` object is for providers that do not support dynamic registration, so it is not included here.

Cursor opens the browser sign-in when the server requires it. This repository's checks did not complete that sign-in.

## vscode.mcp.json

Shape checked against the [VS Code MCP configuration reference](https://code.visualstudio.com/docs/agents/reference/mcp-configuration) for the Copilot harness portable format. That format uses `mcpServers`, `type` `http`, and `url`. The published HTTP example includes `tools`. `"tools": ["*"]` makes the server's tools available; it does not skip tool approval.

Merge the `picsum` entry into `mcpServers` in `$COPILOT_HOME/mcp-config.json`, or `~/.copilot/mcp-config.json` when `COPILOT_HOME` is unset. A workspace-root `.mcp.json` is the documented shared-file destination when VS Code offers it. New Copilot configuration does not go in the deprecated Local harness file `.vscode/mcp.json` (the `servers` document). This example therefore does not use that older shape, and it does not set `oauthClientId`, which the reference documents for a pre-registered OAuth client.

Complete the browser sign-in from the session's server actions when VS Code asks. Authentication stored by another client is not reused.

## gemini.mcpServers.json

This is the `mcpServers` entry to merge into an existing Gemini CLI `settings.json`. It is not a complete settings file. Replacing your settings file with this fragment would drop your other settings.

The same server entry is already loaded by the root [`gemini-extension.json`](../gemini-extension.json) when you install this repository as an extension. Gemini CLI gives a `settings.json` server with the same name precedence over the extension server.

`url` with `type` `http` is the Streamable HTTP form in current Gemini CLI source. `oauth.enabled` is `true` so OAuth is explicitly enabled. Client ID, client secret, issuer, endpoint URLs, and scopes are omitted so the CLI can discover them from the server's 401 challenge and metadata. See the root README for the documentation mismatch around the older `httpUrl` field.

## codex.config.toml

Shape checked against the [Codex MCP guide](https://developers.openai.com/codex/mcp) and the commands published on [https://picsum.org/connect](https://picsum.org/connect). Codex stores remote servers in TOML, not in the JSON shape used above.

Merge this table into `~/.codex/config.toml`, or into `.codex/config.toml` for one trusted project. The equivalent shell command is:

```bash
codex mcp add picsum --url https://picsum.org/mcp
codex mcp login picsum
```

`auth` is omitted because Codex defaults it to stored MCP OAuth credentials. `bearer_token_env_var` is omitted because this flow does not use a pasted bearer token. `--oauth-client-id` is omitted because that flag is for a pre-registered client. A terminal without a local browser can use `codex mcp login picsum --no-browser` and paste the redirect URL back, as described in the Codex guide.

The ChatGPT desktop app and the Codex IDE extension share this Codex configuration. In those interfaces the documented path is Settings, MCP servers, Add server, Streamable HTTP, then the URL `https://picsum.org/mcp`, followed by Authenticate when the server is marked as requiring OAuth. ChatGPT on the web does not read this local file.

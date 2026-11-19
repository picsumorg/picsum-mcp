# Lorem Picsum MCP

Connection guides and client configuration for the hosted Lorem Picsum MCP server.

The server is the remote endpoint **https://picsum.org/mcp**. It searches the Lorem Picsum collection of CC0 photographs and builds exact-size image URLs for layouts and prototypes. It does not generate images from text, and it is not a local stdio package.

This repository distributes English documentation and client configuration. It does not contain the server implementation, the photograph files, account or billing code, or a license for the service or the photographs. The repository owner has not selected a license for these documents, so this repository does not add one.

Lorem Picsum is an independent service inspired by the open-source Picsum Photos project. It is not affiliated with that project, and it has its own catalog and photo IDs. The endpoint above is not `picsum.photos`.

| | |
| --- | --- |
| Homepage | [https://picsum.org/](https://picsum.org/) |
| Connect | [https://picsum.org/connect](https://picsum.org/connect) |
| Privacy | [https://picsum.org/privacy](https://picsum.org/privacy) |
| Terms | [https://picsum.org/terms](https://picsum.org/terms) |
| Pricing | [https://picsum.org/pricing](https://picsum.org/pricing) |
| Cookie policy | [https://picsum.org/cookie](https://picsum.org/cookie) |
| Registry record | [`org.picsum/mcp` 1.0.0](https://registry.modelcontextprotocol.io/v0.1/servers/org.picsum%2Fmcp/versions/1.0.0) |

## Requirements

A client needs all of the following:

- Streamable HTTP, using HTTP POST for JSON-RPC. This server is not an SSE endpoint.
- OAuth 2.1 authorization-code sign-in with PKCE. The authorization server metadata advertises the code challenge method `S256` only.
- Dynamic client registration, or another public-client flow that does not require a client secret copied from this repository. The token endpoint advertises `none` as well as confidential client methods. These examples use discovery and do not embed a client ID or secret.
- A browser on the machine running the client, unless that client documents a separate redirect-paste flow. Sign-in opens the consent page at `https://picsum.org/connect/authorize`.
- The read scope `photos:read`. That is the only scope in the protected-resource metadata.

An unauthenticated `POST` to `https://picsum.org/mcp` on 19 November 2026 returned HTTP 401 with this challenge header:

```http
WWW-Authenticate: Bearer resource_metadata="https://picsum.org/.well-known/oauth-protected-resource/mcp"
```

The response body was a JSON-RPC error, code `-32001`, message `Authorization required.` `GET` and `HEAD` returned HTTP 405 with `Allow: POST, OPTIONS` and no `WWW-Authenticate` header. `OPTIONS` returned HTTP 204. A client that only probes with `GET` or `HEAD` will not see the OAuth challenge.

Those requests checked discovery headers only. They did not register a client, obtain a token, or call a tool.

### Endpoints published by the service

The connect page and the fetched metadata agree on these URLs:

| Purpose | URL |
| --- | --- |
| MCP server | `https://picsum.org/mcp` |
| Protected resource metadata | `https://picsum.org/.well-known/oauth-protected-resource` |
| Path-specific resource metadata (the URL in the 401 challenge) | `https://picsum.org/.well-known/oauth-protected-resource/mcp` |
| Authorization server metadata | `https://picsum.org/.well-known/oauth-authorization-server` |
| Authorization / consent | `https://picsum.org/connect/authorize` |
| Token | `https://picsum.org/api/auth/mcp/token` |
| Dynamic client registration | `https://picsum.org/api/auth/mcp/register` |

Both resource-metadata URLs returned the same document: resource `https://picsum.org/mcp`, authorization server `https://picsum.org`, scope `photos:read`, bearer method `header`, resource name `Lorem Picsum photos`, and documentation `https://picsum.org/connect`.

The authorization server metadata names issuer `https://picsum.org`, response type `code`, grants `authorization_code` and `refresh_token`, and PKCE method `S256`. Its `scopes_supported` list is `openid`, `profile`, `email`, `offline_access`, and `photos:read`. The protected resource advertises only `photos:read`. The retrieved authorization server document does not include `authorization_response_iss_parameter_supported`. These examples do not pin an issuer, a scope list, or a redirect URL, so each client can apply its own discovery rules.

The connect page states that OAuth 2.1 requires PKCE, that clients can register dynamically without a client secret to copy, that each connection opens a consent page, and that access is read-only. It also states that tokens expire after one hour and refresh for up to 30 days. Removing the server from the client is how that page says to disconnect. This repository did not execute that sign-in or refresh cycle.

## Tools

The connect page documents four read-only tools. Parameter details below are the input schemas advertised by the hosted server. This repository did not sign in again to re-list them and did not call them.

### search_photos

Search the CC0 collection by tag, category, or both. Results are paginated and include photo metadata, a ready-to-use image URL, and the total match count. Tags match word prefixes (`cof` matches coffee).

| Parameter | Required | Constraint |
| --- | --- | --- |
| `tag` | No | String, up to 80 characters |
| `category` | No | One category ID from the list below |
| `page` | No | Integer, minimum 1, default 1 |
| `limit` | No | Integer, 1 to 30, default 10 |

### get_photo

Look up one photo by ID: author, description, category, tags, dimensions, source link, and CC0 license.

| Parameter | Required | Constraint |
| --- | --- | --- |
| `id` | Yes | Photo ID string |

### list_categories

List every category ID with its display name and group. This tool takes no parameters. The category IDs accepted by `search_photos` and `build_image_url` are:

`coasts`, `deserts`, `freshwater`, `gardens`, `landscapes`, `macro`, `mountains`, `plants`, `skies`, `snow`, `woodlands`, `animals`, `birds`, `insects`, `marine`, `pets`, `aerial`, `architecture`, `city`, `interiors`, `landmarks`, `night`, `transport`, `agriculture`, `food`, `industry`, `music`, `objects`, `sculpture`, `sports`, `technology`, `textures`, `workspaces`.

### build_image_url

Build an exact-size image URL and an HTML `img` snippet. Width and height go up to 2000 pixels. Omit height for a square. Use `photo_id` to pin one photo, `seed` for a repeatable choice, or neither for a random photo. The seed also acts as a subject word, so seed `cat` selects a cat photo. `tag` narrows random choices. `category` narrows random and seeded choices. Grayscale, blur from 1 to 10, and WebP are supported. JPEG is the default.

The tool description states that every size, grayscale, and blur is free, that the six preset sizes are pre-rendered, and that another size is rendered on the first request and then cached. It also states that a custom size, grayscale, or blur returns a URL pinned to one photo. The preset sizes named by the tool are 800×600, 640×640, 1200×800, 600×800, 1280×720, and 1920×1080.

| Parameter | Required | Constraint |
| --- | --- | --- |
| `width` | Yes | Integer, 1 to 2000 |
| `height` | No | Integer, 1 to 2000 |
| `photo_id` | No | String |
| `seed` | No | String, up to 100 characters |
| `tag` | No | String, up to 80 characters |
| `category` | No | One category ID from the list above |
| `format` | No | `jpg` (default) or `webp` |
| `grayscale` | No | Boolean, default false |
| `blur` | No | Integer, 1 to 10 |

A random image URL without a photo ID or seed can change from request to request. Image URLs and the MCP tools are different interfaces: the website documents ordinary image URLs under `https://picsum.org/`, while this server speaks MCP at `https://picsum.org/mcp`.

## Access, photographs, and accounts

The terms of service dated 16 November 2026 cover the website, the random image generator, the image URL API, and the MCP server. They state that JPEG and WebP image requests are free, and that an account or API key is unnecessary for custom sizes, grayscale, or blur. An account is required to create and manage API keys. The terms allow the service to be changed, limited, or discontinued, and they prohibit working around rate limits and credit charges. The homepage says to follow the `Retry-After` header when an image response is HTTP 429. No numeric MCP rate limit was published on the pages read for this guide.

The pricing page, retrieved 19 November 2026, repeats that custom sizes, grayscale, and blur do not require an account or API key. It also lists one-time credit packs in US dollars: Starter at $9.90 for 1,000 credits, Pro at $19.90 for 2,200 credits, and Ultimate at $49.90 for 6,000 credits. Each paid pack was labeled "Purchase unavailable." That page says purchased credits do not expire. The terms also say credits have no cash value, are not transferable, and may be adjusted or expire as described where they are sold or granted. This repository does not sell credits or API keys, and the connect page does not publish a per-call credit price for MCP tools. The privacy policy states that a signed-in account has a recorded credit balance, credit history, and any API keys created for that account. Use the live [terms](https://picsum.org/terms) and [pricing](https://picsum.org/pricing) pages for current access terms.

The photographs are designated CC0 for personal and commercial use. Attribution is optional, and each photo links to its source. The terms say source records are not guaranteed, so a sensitive use should be checked at the original source. Photographs of identifiable people or trademarks can involve rights outside copyright, and those rights remain the user's responsibility. Nothing in this repository licenses the photographs, the MCP server, or the image API.

The privacy policy dated 15 November 2026 describes account data, sign-in cookies, and technical request data for the website, image API, and MCP server. Questions can go to the contact address published there, hello@picsum.org.

## Connect a client

Install or merge one example, then complete that client's browser sign-in. Do not paste an access token, refresh token, client secret, or API key into these files. Client-specific copy instructions are in [clients/README.md](clients/README.md).

### Claude Code

Documented on the connect page and in the [Claude Code MCP guide](https://code.claude.com/docs/en/mcp):

```bash
claude mcp add --transport http picsum https://picsum.org/mcp
```

In Claude Code, run `/mcp`, select `picsum`, and authenticate. `claude mcp login picsum` runs the same OAuth flow from the shell. The project-file form is [clients/claude-code.mcp.json](clients/claude-code.mcp.json). `type` must be `http`.

### Codex

Documented on the connect page and in the [Codex MCP guide](https://developers.openai.com/codex/mcp):

```bash
codex mcp add picsum --url https://picsum.org/mcp
codex mcp login picsum
```

The TOML form for `~/.codex/config.toml` is [clients/codex.config.toml](clients/codex.config.toml). Remote MCP login requires a Codex CLI that supports it, as the connect page notes. The ChatGPT desktop app and the Codex IDE extension share this configuration: add a Streamable HTTP server with the URL above, then choose Authenticate. ChatGPT on the web does not read that local file.

### Cursor

Merge [clients/cursor.mcp.json](clients/cursor.mcp.json) into `mcpServers` in `~/.cursor/mcp.json` or `.cursor/mcp.json`. The [Cursor MCP documentation](https://cursor.com/docs/mcp) uses `url` for a remote Streamable HTTP server and supports OAuth with dynamic client registration for a public client. No static `auth` object is included, because that object is for a provider-issued client ID.

### VS Code with Copilot

Merge [clients/vscode.mcp.json](clients/vscode.mcp.json) into the portable `mcpServers` document described in the [VS Code MCP configuration reference](https://code.visualstudio.com/docs/agents/reference/mcp-configuration): `$COPILOT_HOME/mcp-config.json`, or `~/.copilot/mcp-config.json` when `COPILOT_HOME` is unset. Approve the browser sign-in when the session asks. The example does not set `oauthClientId`.

### Grok Bot

The connect page documents these settings and no JSON file:

```text
Name: picsum
URL: https://picsum.org/mcp
Transport: Streamable HTTP
Auth: OAuth
```

Sign in when the bot prompts. It discovers the OAuth endpoints and registers its client. Menu names vary.

### Other clients

The connect page says other MCP clients can connect when they support OAuth with dynamic client registration. Use Streamable HTTP against `https://picsum.org/mcp`, and let the client discover the resource metadata from the 401 challenge. Do not point these instructions at a third-party stdio package.

## Gemini CLI extension

Current Gemini CLI can connect to this remote OAuth server. The root manifest [`gemini-extension.json`](gemini-extension.json) loads one Streamable HTTP server named `picsum`:

- `url` is `https://picsum.org/mcp`
- `type` is `http`, which current Gemini CLI source maps to Streamable HTTP
- `oauth.enabled` is `true`
- client ID, client secret, issuer, endpoint URLs, and scopes are omitted so discovery can fill them in

The transport choice follows `createUrlTransport` in [`packages/core/src/tools/mcp-client.ts`](https://github.com/google-gemini/gemini-cli/blob/main/packages/core/src/tools/mcp-client.ts) as retrieved on 19 November 2026. In that source, `httpUrl` still selects Streamable HTTP but is deprecated, and a bare `url` without `type` also defaults to Streamable HTTP. The public page [MCP servers with Gemini CLI](https://geminicli.com/docs/tools/mcp-server/) still describes the older split, where `url` means SSE and `httpUrl` means HTTP streaming. This manifest uses the non-deprecated `url` plus `type: "http"` form. A Gemini CLI build that only understands `url` as SSE would not speak this server's protocol: `GET` on the endpoint returns 405. This repository did not install Gemini CLI or complete its browser sign-in.

OAuth discovery in that source proceeds from a 401 and `WWW-Authenticate` header, with a fallback to authorization-server metadata. `oauth.enabled` is set because the same source gates part of the fallback on that flag. The [Gemini CLI OAuth section](https://geminicli.com/docs/tools/mcp-server/) also says a local browser and a loopback redirect are required. The manifest does not set `trust`. Extension server configuration supports the usual MCP server fields except `trust`, per the [extension reference](https://geminicli.com/docs/extensions/reference/).

Install from a shell, with Git available:

```bash
gemini extensions install https://github.com/picsumorg/picsum-mcp
```

Restart Gemini CLI after installation. If the browser sign-in does not start on its own, run `/mcp auth picsum`. The server key is `picsum`. The extension name is `picsum-mcp`, matching this repository's name. [`GEMINI.md`](GEMINI.md) is the extension context file. Users who would rather merge the server into `settings.json` can use [clients/gemini.mcpServers.json](clients/gemini.mcpServers.json). A server of the same name in `settings.json` overrides the extension.

The extension `version` is `1.0.0`, the same version string as the already published registry server record. That match identifies this configuration package. It is not a new server release, and installing the extension does not publish or change the registry.

### Gallery discovery

Direct installation uses the GitHub URL and does not require a GitHub topic. Listing in the Gemini CLI extension gallery does. The [extension release guide](https://geminicli.com/docs/extensions/releasing/) says the gallery crawler finds a public repository that has the topic `gemini-cli-extension` and a `gemini-extension.json` file at the repository root. This repository does not set that topic. Adding it is a GitHub About setting for a maintainer. It is not done from this documentation, and it does not install an application.

## Official registry

`org.picsum/mcp` version `1.0.0` is already published and marked latest. The record was retrieved on 19 November 2026 from the official registry API. It describes a Streamable HTTP remote at `https://picsum.org/mcp` and points its website URL at `https://picsum.org/connect`. Status was `active`, published at `2026-11-18T13:24:14.966893Z`.

This repository does not include a `server.json`, and it does not submit, replace, or edit that registry record.

## Configuration checks

Local checks validate the files in this repository. They do not sign in, register an OAuth client, or call the MCP tools.

```bash
python3 scripts/validate_configs.py
jq empty gemini-extension.json clients/*.json
python3 -c 'import tomllib; tomllib.load(open("clients/codex.config.toml","rb"))'
```

Results on 19 November 2026, Python 3.12.3:

- `python3 scripts/validate_configs.py` exited 0. It parsed five JSON documents and `clients/codex.config.toml`, required the hosted endpoint, and found no credential keys.
- `jq empty` on `gemini-extension.json` and every `clients/*.json` file exited 0.
- `tomllib` parsed `clients/codex.config.toml` and exited 0.

The separate header checks against `https://picsum.org/mcp` and the well-known metadata URLs are described under Requirements. They were unauthenticated `curl` requests and are not repeated by the local script.

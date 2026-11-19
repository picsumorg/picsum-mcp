# Lorem Picsum

This extension connects to the hosted Lorem Picsum MCP server at https://picsum.org/mcp. The server searches the CC0 photograph collection and builds exact-size image URLs. It does not generate images from text.

Access is read-only. The protected-resource metadata advertises the scope `photos:read`. Sign-in uses OAuth discovery. This extension does not contain a client secret, access token, or API key.

Use the server tools for photo lookup and image URLs:

- `search_photos` searches by tag, category, or both.
- `get_photo` reads one photo record by ID.
- `list_categories` lists category IDs, display names, and groups.
- `build_image_url` builds an exact-size image URL and an HTML `img` snippet.

Width and height are integers from 1 to 2000. Omitting height requests a square. Formats are JPEG by default and WebP when requested. A photo ID or seed repeats a chosen photo. A URL with neither can change between requests.

Lorem Picsum designates the photographs CC0. Attribution is optional. Identifiable people and trademarks can involve rights outside copyright. This extension does not license the photographs or the hosted service.

Published service terms, pricing, and privacy are at https://picsum.org/terms, https://picsum.org/pricing, and https://picsum.org/privacy. Do not invent access limits, credit prices, or availability.

# MCPTTS

Make Claude speak using MCP

[![CleanShot 2025-04-02 at 08 00 05@2x](https://github.com/user-attachments/assets/5e1dee79-0e21-48bf-9952-a0619aafddb4)](https://www.loom.com/share/febbe046bb43488dbebe9c0348cbc690)

## Installation


### Using uv

Clone this repo (say, into `/mcp/mcptts`)

```bash
# Create and activate virtual environment
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

## Setting up with Claude


Add the following configuration to Claude's config JSON file:
```json
{
  "tts": {
    "command": "/mcp/mcptts/.venv/bin/python",
    "args": ["/mcp/mcptts/mcp_server.py"]
  }
}
```

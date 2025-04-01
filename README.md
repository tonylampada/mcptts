# MCPTTS

A simple Python package that enables Claude to speak through your Mac's text-to-speech system.

## What it does

MCPTTS provides a lightweight wrapper around macOS's built-in text-to-speech capabilities and exposes it via the Model Context Protocol (MCP). This allows Claude and other AI assistants to speak through your computer's audio.

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

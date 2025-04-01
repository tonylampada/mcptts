#!/usr/bin/env python3

from mcp.server.fastmcp import FastMCP, Context
from tts import say, list_voices

mcp = FastMCP("Mac TTS")

@mcp.tool()
def quick_speak(text: str) -> str:
    say(text, voice="Samantha")
    return f"Spoke text using default voice (Samantha)"

if __name__ == "__main__":
    mcp.run()

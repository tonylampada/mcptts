#!/usr/bin/env python3

from mcp.server.fastmcp import FastMCP, Context
import tts

mcp = FastMCP("Mac TTS")

@mcp.tool()
def quick_speak(text: str, language: str) -> str:
    en = {'voice': 'Samantha', 'rate': 180}
    pt = {'voice': 'Luciana', 'rate': 200}

    kwargs = {
        'en': en,
        'en-us': en,
        'en_us': en,
        'pt': pt,
        'pt-br': pt,
        'pt_br': pt,
        'pt-pt': pt,
        'pt_pt': pt,
    }[language.lower()]
    tts.async_say(text, **kwargs)
    return f"Spoke text using language {language}"

if __name__ == "__main__":
    mcp.run()

#!/usr/bin/env python3
import subprocess
import platform
from typing import Optional, List


def _build_say_command(text: str, voice: Optional[str] = None, rate: Optional[int] = None, volume: Optional[float] = None) -> List[str]:
    if platform.system() != "Darwin":
        raise OSError("This function only works on macOS")
    command = ["say"]
    if voice:
        command.extend(["-v", voice])
    if rate:
        command.extend(["-r", str(rate)])
    if volume is not None:
        vol_percent = int(volume * 100)
        command.extend(["-v", str(vol_percent)])
    command.append(text)
    return command

def say(text, voice=None, rate=None, volume=None):
    command = _build_say_command(text, voice, rate, volume)
    return subprocess.call(command)


def list_voices():
    if platform.system() != "Darwin":
        raise OSError("This function only works on macOS")
    result = subprocess.run(["say", "-v", "?"], capture_output=True, text=True)
    voices = []
    for line in result.stdout.strip().split('\n'):
        parts = line.split()
        if parts:
            voices.append(parts[0])
    return sorted(set(voices))


if __name__ == "__main__":
    print("Testing the text-to-speech functionality...")
    say("Hello, this is a test of the Mac text to speech system.")
    print("\nAvailable voices:")
    voices = list_voices()
    for voice in voices[:10]:
        print(f"Voice: {voice}")
        say(f"Hello, this is the {voice} voice.", voice=voice)
    print("\nAll speech completed.")

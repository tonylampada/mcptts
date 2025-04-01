#!/usr/bin/env python3
"""
Mac Text-to-Speech Module

This module provides a simple interface to macOS's text-to-speech functionality.
"""

import subprocess
import platform

def say(text, voice=None, rate=None, volume=None):
    """
    Speak the provided text using macOS text-to-speech.
    
    Args:
        text (str): The text to be spoken
        voice (str, optional): The voice to use (e.g., "Alex", "Samantha", "Daniel")
        rate (int, optional): Speaking rate (words per minute)
        volume (float, optional): Volume from 0.0 to 1.0
    
    Returns:
        int: Return code from the say command
    """
    # Check if running on macOS
    if platform.system() != "Darwin":
        raise OSError("This function only works on macOS")
    
    # Build the command
    command = ["say"]
    
    if voice:
        command.extend(["-v", voice])
    
    if rate:
        command.extend(["-r", str(rate)])
        
    if volume is not None:
        # Convert 0.0-1.0 to 0-100 for the say command
        vol_percent = int(volume * 100)
        command.extend(["-v", str(vol_percent)])
    
    # Add the text to speak
    command.append(text)
    
    # Execute the command
    return subprocess.call(command)

def list_voices():
    """
    List all available voices on the system.
    
    Returns:
        list: A list of available voice names
    """
    if platform.system() != "Darwin":
        raise OSError("This function only works on macOS")
    
    # Get the list of voices
    result = subprocess.run(["say", "-v", "?"], capture_output=True, text=True)
    
    # Parse the output
    voices = []
    for line in result.stdout.strip().split('\n'):
        parts = line.split()
        if parts:
            voices.append(parts[0])
    
    return sorted(set(voices))

if __name__ == "__main__":
    # Simple demo
    print("Testing the text-to-speech functionality...")
    say("Hello, this is a test of the Mac text to speech system.")
    
    print("\nAvailable voices:")
    voices = list_voices()
    for voice in voices[:50]:  # Show first 5 voices
        print(f"Voice: {voice}")
        say(f"Hello, this is the {voice} voice.", voice=voice)

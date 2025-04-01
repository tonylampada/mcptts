#!/usr/bin/env python3
"""
Test script for the Mac TTS module
"""

from tts import say, list_voices

if __name__ == "__main__":
    # Basic test
    say("Hello! This is a test of the text to speech system.")
    
    # Test with different voice
    say("This is a different voice speaking.", voice="Samantha")
    
    # Test with adjusted rate
    say("This is speech at a slower rate.", rate=120)
    
    # Test with adjusted volume
    say("This is speech at a lower volume.", volume=0.5)
    
    # Print some available voices
    print("Some available voices:")
    voices = list_voices()
    for voice in voices[:5]:
        print(f"- {voice}")

#!/usr/bin/env python3
"""
Mac Text-to-Speech Module

This module provides a simple interface to macOS's text-to-speech functionality.
"""

import subprocess
import platform
import threading
import queue
from typing import Optional, List, NamedTuple
from dataclasses import dataclass

@dataclass
class SpeechRequest:
    """A request to speak text with specific parameters"""
    text: str
    voice: Optional[str] = None
    rate: Optional[int] = None
    volume: Optional[float] = None
    process: Optional[subprocess.Popen] = None

# Global state for speech queue management
_speech_queue = queue.Queue()
_speech_thread = None
_current_process: Optional[subprocess.Popen] = None
_should_run = True

def _build_say_command(text: str, voice: Optional[str] = None, rate: Optional[int] = None, volume: Optional[float] = None) -> List[str]:
    """
    Build the say command with the given parameters.
    
    Args:
        text (str): The text to be spoken
        voice (str, optional): The voice to use (e.g., "Alex", "Samantha", "Daniel")
        rate (int, optional): Speaking rate (words per minute)
        volume (float, optional): Volume from 0.0 to 1.0
    
    Returns:
        List[str]: The command as a list of arguments
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
    
    return command

def _process_speech_queue():
    """Background thread function to process speech requests"""
    global _current_process, _should_run
    
    while _should_run:
        try:
            # Get the next speech request, waiting if queue is empty
            request = _speech_queue.get()
            
            # Build and execute the command
            command = _build_say_command(request.text, request.voice, request.rate, request.volume)
            
            # If there's an existing process, wait for it to finish
            if _current_process is not None:
                _current_process.wait()
            
            # Start the new process
            _current_process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Store the process in the request object
            request.process = _current_process
            
            # Wait for this speech to finish
            _current_process.wait()
            _current_process = None
            
            # Mark the task as done
            _speech_queue.task_done()
            
        except queue.Empty:
            continue
        except Exception as e:
            print(f"Error in speech thread: {e}")
            continue

def _ensure_speech_thread():
    """Ensure the speech processing thread is running"""
    global _speech_thread, _should_run
    
    if _speech_thread is None or not _speech_thread.is_alive():
        _should_run = True
        _speech_thread = threading.Thread(target=_process_speech_queue, daemon=True)
        _speech_thread.start()

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
    command = _build_say_command(text, voice, rate, volume)
    return subprocess.call(command)

def async_say(text, voice=None, rate=None, volume=None):
    """
    Asynchronously speak the provided text using macOS text-to-speech.
    Multiple calls will be queued and processed in order.
    
    Args:
        text (str): The text to be spoken
        voice (str, optional): The voice to use (e.g., "Alex", "Samantha", "Daniel")
        rate (int, optional): Speaking rate (words per minute)
        volume (float, optional): Volume from 0.0 to 1.0
    
    Returns:
        SpeechRequest: An object representing the queued speech request
    """
    # Ensure the processing thread is running
    _ensure_speech_thread()
    
    # Create and queue the request
    request = SpeechRequest(text, voice, rate, volume)
    _speech_queue.put(request)
    
    return request

def stop_all():
    """Stop all pending speech and shutdown the speech thread"""
    global _should_run, _current_process, _speech_thread
    
    # Signal the thread to stop
    _should_run = False
    
    # Clear the queue
    while not _speech_queue.empty():
        try:
            _speech_queue.get_nowait()
            _speech_queue.task_done()
        except queue.Empty:
            break
    
    # Stop current speech if any
    if _current_process is not None:
        _current_process.terminate()
        _current_process.wait()
        _current_process = None
    
    # Wait for the thread to finish
    if _speech_thread is not None:
        _speech_thread.join()
        _speech_thread = None

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

def wait_until_done():
    """Wait for all queued speech requests to complete."""
    _speech_queue.join()

if __name__ == "__main__":
    # Simple demo
    print("Testing the text-to-speech functionality...")
    async_say("Hello, this is a test of the Mac text to speech system.")
    wait_until_done()
    
    print("\nAvailable voices:")
    voices = list_voices()
    for voice in voices[:10]:  # Show first 5 voices
        print(f"Voice: {voice}")
        async_say(f"Hello, this is the {voice} voice.", voice=voice)
    
    # Wait for all voices to finish speaking
    wait_until_done()
    print("\nAll speech completed.")

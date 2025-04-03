#!/usr/bin/env python3
import subprocess
import platform
import threading
import queue
from typing import Optional, List, NamedTuple
from dataclasses import dataclass

@dataclass
class SpeechRequest:
    text: str
    voice: Optional[str] = None
    rate: Optional[int] = None
    volume: Optional[float] = None
    process: Optional[subprocess.Popen] = None

_speech_queue = queue.Queue()
_speech_thread = None
_current_process: Optional[subprocess.Popen] = None
_should_run = True

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

def _process_speech_queue():
    global _current_process, _should_run
    while _should_run:
        try:
            request = _speech_queue.get()
            command = _build_say_command(request.text, request.voice, request.rate, request.volume)
            if _current_process is not None:
                _current_process.wait()
            _current_process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            request.process = _current_process
            _current_process.wait()
            _current_process = None
            _speech_queue.task_done()
        except queue.Empty:
            continue
        except Exception as e:
            print(f"Error in speech thread: {e}")
            continue

def _ensure_speech_thread():
    global _speech_thread, _should_run
    if _speech_thread is None or not _speech_thread.is_alive():
        _should_run = True
        _speech_thread = threading.Thread(target=_process_speech_queue, daemon=True)
        _speech_thread.start()

def say(text, voice=None, rate=None, volume=None):
    command = _build_say_command(text, voice, rate, volume)
    return subprocess.call(command)

def async_say(text, voice=None, rate=None, volume=None):
    _ensure_speech_thread()
    request = SpeechRequest(text, voice, rate, volume)
    _speech_queue.put(request)
    return request

def stop_all():
    global _should_run, _current_process, _speech_thread
    _should_run = False
    while not _speech_queue.empty():
        try:
            _speech_queue.get_nowait()
            _speech_queue.task_done()
        except queue.Empty:
            break
    if _current_process is not None:
        _current_process.terminate()
        _current_process.wait()
        _current_process = None
    if _speech_thread is not None:
        _speech_thread.join()
        _speech_thread = None

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

def wait_until_done():
    _speech_queue.join()

if __name__ == "__main__":
    print("Testing the text-to-speech functionality...")
    async_say("Hello, this is a test of the Mac text to speech system.")
    wait_until_done()
    print("\nAvailable voices:")
    voices = list_voices()
    for voice in voices[:10]:
        print(f"Voice: {voice}")
        async_say(f"Hello, this is the {voice} voice.", voice=voice)
    wait_until_done()
    print("\nAll speech completed.")

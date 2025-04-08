import requests
import pyaudio
import wave
import io
import tempfile
import os
import subprocess

# Server info
server = "http://jarbas.tail925c5f.ts.net:5002"

speakers = [
    'Claribel Dervla', 'Daisy Studious', 'Gracie Wise', 'Tammie Ema', 'Alison Dietlinde', 'Ana Florence', 
    'Annmarie Nele', 'Asya Anara', 'Brenda Stern', 'Gitta Nikolina', 'Henriette Usha', 'Sofia Hellen', 
    'Tammy Grit', 'Tanja Adelina', 'Vjollca Johnnie', 'Andrew Chipper', 'Badr Odhiambo', 'Dionisio Schuyler', 
    'Royston Min', 'Viktor Eka', 'Abrahan Mack', 'Adde Michal', 'Baldur Sanjin', 'Craig Gutsy', 'Damien Black', 
    'Gilberto Mathias', 'Ilkin Urbano', 'Kazuhiko Atallah', 'Ludvig Milivoj', 'Suad Qasim', 'Torcull Diarmuid', 
    'Viktor Menelaos', 'Zacharie Aimilios', 'Nova Hogarth', 'Maja Ruoho', 'Uta Obando', 'Lidiya Szekeres', 
    'Chandra MacFarland', 'Szofi Granger', 'Camilla Holmström', 'Lilya Stainthorpe', 'Zofija Kendrick', 
    'Narelle Moon', 'Barbora MacLean', 'Alexandra Hisakawa', 'Alma María', 'Rosemary Okafor', 'Ige Behringer', 
    'Filip Traverse', 'Damjan Chapman', 'Wulf Carlevaro', 'Aaron Dreschner', 'Kumar Dahl', 'Eugenio Mataracı', 
    'Ferran Simen', 'Xavier Hayasaka', 'Luis Moray', 'Marcos Rudaski']


def get_wav(text, language="en"):
    params = {"text": text, "language_id": language, "speaker_id": 'Tanja Adelina'}
    response = requests.get(f"{server}/api/tts", params=params)
    if response.status_code != 200:
        print(f"Error: {response.status_code} {response.text}")
        import traceback
        traceback.print_exc()
        raise Exception(f"Error: {response.status_code} {response.text}")
    return response.content

p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(2), channels=1, rate=22050, output=True)


def play_wave_file(filepath):
    wf = wave.open(filepath, 'rb')
    audio_data = wf.readframes(wf.getnframes())
    stream.write(audio_data)
    wf.close()

def say(text, language="en"):
    print(f"will say {text} using language {language}")
    wav = get_wav(text, language)
    print(f"got wav {text} using language {language}")
    with tempfile.TemporaryDirectory() as tmpdir:
        orig_wav = os.path.join(tmpdir, "original.wav")
        with open(orig_wav, "wb") as f:
            f.write(wav)
        
        fast_wav = os.path.join(tmpdir, "fast.wav")
        subprocess.run([
            "ffmpeg", "-i", orig_wav,
            "-filter:a", "atempo=1.35",
            "-y", fast_wav
        ], check=True)
        
        play_wave_file(fast_wav)


def save(text, language, wavout):
    wav = get_wav(text, language)
    with open(wavout, "wb") as f:
        f.write(wav)

if __name__ == "__main__":
    say("Hello, world!")

import requests
import pyaudio
import wave
import io

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


def play_wave_bytes(wave_bytes):
    wav_buffer = io.BytesIO(wave_bytes)
    with wave.open(wav_buffer, 'rb') as wav_file:
        audio_data = wav_file.readframes(wav_file.getnframes())
        stream.write(audio_data)

def say(text, language="en"):
    print(f"will say {text} using language {language}")
    wav = get_wav(text, language)
    print(f"got wav {text} using language {language}")
    try:
        play_wave_bytes(wav)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


def save(text, language, wavout):
    wav = get_wav(text, language)
    with open(wavout, "wb") as f:
        f.write(wav)

if __name__ == "__main__":
    say("Hello, world!")

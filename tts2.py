import numpy as np
import pyaudio
from TTS.api import TTS

import torch
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import XttsAudioConfig, XttsArgs
from TTS.config.shared_configs import BaseDatasetConfig
from TTS.utils.radam import RAdam
from collections import defaultdict
from builtins import dict
import os
torch.serialization.add_safe_globals([XttsConfig, XttsAudioConfig, XttsArgs, BaseDatasetConfig, RAdam, defaultdict, dict])

print("Loading TTS model...")

models = [
    "tts_models/en/ljspeech/tacotron2-DDC",
    "tts_models/en/ljspeech/glow-tts",
    "tts_models/en/ljspeech/fast_pitch",
    "tts_models/en/ljspeech/tacotron2-DCA",
    "tts_models/en/ljspeech/vits",
]

models_need_speaker = [
    "tts_models/en/vctk/vits",
    "tts_models/multilingual/multi-dataset/your_tts",
    "tts_models/multilingual/multi-dataset/xtts_v2",
    "tts_models/multilingual/multi-dataset/xtts_v1.1",
]

models_need_language = [
]


# model = "tts_models/en/ljspeech/tacotron2-DDC"
# model = "tts_models/
# multilingual/multi-dataset/xtts_v2"
# model = "tts_models/multilingual/multi-dataset/xtts_v2"
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
# print(model)

# speakers = tts.speakers
# print(speakers)

# print("Initializing PyAudio...")
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=22050, output=True)

current_dir = os.path.dirname(os.path.abspath(__file__))

def say(text, language="en", wav='peterson_cut.wav'):
    wav = tts.tts(text, speaker_wav=f"{current_dir}/{wav}", language=language)
    # wav = tts.tts(text)
    stream.write(np.array(wav, dtype=np.float32).tobytes())

def save(text, modelname, wavout):
    tts = TTS(modelname)
    wav = tts.tts(text, speaker_wav="./scarlet_cut.wav", language="en")
    # wav = tts.tts(text)
    import soundfile as sf
    sf.write(wavout, wav, 22050)

# def bye():
#     stream.stop_stream()
#     stream.close()
#     p.terminate()

def saveall():
    import logging
    logging.getLogger("").setLevel(logging.ERROR)
    _models = models + models_need_speaker + models_need_language
    _models = models_need_speaker
    # _models = ["tts_models/multilingual/multi-dataset/xtts_v1"]
    for modelname in _models:
        try:
            modelnameout = modelname.replace("/", "_")
            text = "The North Wind and the Sun were disputing which was the stronger, when a traveler came along wrapped in a warm cloak. They agreed that the one who first succeeded in making the traveler take his cloak off should be considered stronger than the other. Then the North Wind blew as hard as he could, but the more he blew the more closely did the traveler fold his cloak around him; and at last the North Wind gave up the attempt. Then the Sun shined out warmly, and immediately the traveler took off his cloak. And so the North Wind was obliged to confess that the Sun was the stronger of the two."
            save(text, modelname, f"out_{modelnameout}.wav")
            print(f"EEEEEEE ok [{modelname}]")
        except Exception as e:
            print(f"EEEEEEEEEError [{modelname}]: {e}")

if __name__ == "__main__":
    # silence python logging
    say("The quick brow fox jumps over the lazy dog", speed=2.5)
        # save("This is a test of the text to speech system.", "output_save.wav")
        # bye()

    # Cleanup (optional, if you want to close after one use)

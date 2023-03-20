import torch
import sounddevice as sd
import time

import os
import torch

def test():
    device = torch.device('cpu')
    torch.set_num_threads(4)
    local_file = 'model.pt'

    if not os.path.isfile(local_file):
        torch.hub.download_url_to_file('https://models.silero.ai/models/tts/ru/v3_1_ru.pt',
                                       local_file)

    model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
    model.to(device)

    example_text = 'В недрах тундры выдры в г+етрах т+ырят в вёдра ядра кедров.'
    sample_rate = 48000
    speaker='baya'

    audio_paths = model.save_wav(text=example_text,
                                 speaker=speaker,
                                 sample_rate=sample_rate)
"""language = 'ru'
model_id = 'ru_v3'

sample_rate = 48000 # 48000
speaker = 'random' # aidar, baya, kseniya, xenia, random
put_accent = True
put_yo = True
device = torch.device('cpu')# cpu или gpu

model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                          model='silero_tts',
                          language=language,
                          speaker=model_id)
model.to(device)


def random_speak(what: str):
    sample_rate = 48000
    speaker = 'random'

    example_text = 'В недрах тундры выдры в г+етрах т+ырят в вёдра ядра к+едров.'

    audio = model.apply_tts(text=example_text,
                            speaker=speaker,
                            sample_rate=sample_rate)


def va_speak(what: str):
    audio = model.apply_tts(text=what+"..",
                            speaker=speaker,
                            sample_rate=sample_rate,
                            put_accent=put_accent,
                            put_yo=put_yo)

    sd.play(audio, sample_rate * 0.95)
    time.sleep((len(audio) / (sample_rate * 0.95)))
    sd.stop()




language = 'ru'
model_id = 'ru_v3'

sample_rate = 48000 # 48000
speaker = 'random' # aidar, baya, kseniya, xenia, random
put_accent = True
put_yo = True
device = torch.device('cpu')# cpu или gpu

model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                          model='silero_tts',
                          language=language,
                          speaker=model_id)
model.to(device)


# воспроизводим
def va_speak(what: str):
    audio = model.apply_tts(text=what+"..",
                            speaker=speaker,
                            sample_rate=sample_rate,
                            put_accent=put_accent,
                            put_yo=put_yo)

    sd.play(audio, sample_rate * 0.95)
    time.sleep((len(audio) / (sample_rate * 0.95)))
    sd.stop()"""

# sd.play(audio, sample_rate)
# time.sleep(len(audio) / sample_rate)
# sd.stop()
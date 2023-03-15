import threading

import vosk
import sys
import sounddevice as sd
import queue

model = vosk.Model("model")
samplerate = 16000
q = queue.Queue()
device = 2


def q_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


def va_listen():
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device, dtype='int16',
                           channels=1, callback=q_callback):

        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                print(rec.Result())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(1)
    task_listen = threading.Thread(name="listen_step_1", target=va_listen)
    task_listen.start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

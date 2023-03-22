import threading

import vosk
import sys
import sounddevice as sd
import queue
import speaker
import stt_silero

model = vosk.Model("model_s")
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


if __name__ == '__main__':
    #stt_silero.silero_stt_test()
    #speaker.test_ru()
    speaker.test_en()
    #speaker.va_speak('Съ+ешьте ещ+ё +этих м+ягких франц+узских б+улочек, д+а в+ыпейте ч+аю.')
    #task_listen = threading.Thread(name="listen_step_1", target=va_listen)
    #task_listen.start()


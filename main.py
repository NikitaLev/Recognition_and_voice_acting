import json
import os
import threading
import wave

from fuzzywuzzy import fuzz

import vosk
import sys
import sounddevice as sd
import queue
import speaker
import stt_silero
from glob import glob

model = vosk.Model("model_s")
samplerate = 16000
q = queue.Queue()
device = 2
str_ex = 'the birch canoe slid on the smooth planks glue the sheet to the dark blue background it\'s easy to tell the ' \
         'depth of a well four hours of steady work faced us'


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


def get_text_from_voice(filename):
    wf = wave.open(filename, "rb")

    rec = vosk.KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    text_lst = []
    p_text_lst = []
    p_str = []
    len_p_str = []
    while True:
        data = wf.readframes(16000)
        if len(data) == 0:
            p_text_lst.append(rec.PartialResult())
            p_text_lst.append(rec.PartialResult())
            break
        if rec.AcceptWaveform(data):
            text_lst.append(rec.Result())
            print(1, rec.Result())
        else:
            p_text_lst.append(rec.PartialResult())
            #print(2, rec.PartialResult())

    #print(1, rec.Result())
    if len(text_lst) != 0:
        jd = json.loads(text_lst[0])
        txt_str = jd["text"]

    elif len(p_text_lst) != 0:
        for i in range(0, len(p_text_lst)):
            temp_txt_dict = json.loads(p_text_lst[i])
            p_str.append(temp_txt_dict['partial'])

        len_p_str = [len(p_str[j]) for j in range(0, len(p_str))]
        max_val = max(len_p_str)
        indx = len_p_str.index(max_val)
        txt_str = p_str[indx]

    else:
        txt_str = ''
    pr = recognize_cmd(txt_str, 'vosk')
    print(filename)
    print('vosk = ', txt_str)
    print('orig = ', str_ex)
    print('% = ', pr)
    print()
    return txt_str


def recognize_cmd(cmd: str, name):
    rc = {'name': '', 'percent': 0}
    # print('rc', rc)
    vrt = fuzz.ratio(cmd, str_ex)
    rc['name'] = name
    rc['percent'] = vrt
    # print(x + ' x = '+str(vrt))
    return vrt


def silero_test(filename):
    res = stt_silero.silero_stt_test(filename)
    pr = recognize_cmd(res, 'silero')
    print(filename)
    print('silero = ', res)
    print('orig   = ', str_ex)
    print('% = ', pr)
    print()
    return


if __name__ == '__main__':
    name_file1 = 'en_sample_1_16k.wav'
    params1 = {"filename": name_file1}
    task_file1 = threading.Thread(name="listen_silero_1", target=silero_test, kwargs=params1)
    task_file1.start()
    """
    speaker.va_speak('Съ+ешьте ещ+ё +этих м+ягких франц+узских б+улочек, д+а в+ыпейте ч+аю.')
    name_file1 = 'en_sample_1_8k.wav'
    params1 = {"filename": name_file1}
    task_file1 = threading.Thread(name="listen_silero_1", target=silero_test, kwargs=params1)
    task_file1.start()

        name_file2 = 'en_sample_1_16k.wav'
    params2 = {"filename": name_file2}
    task_file2 = threading.Thread(name="listen_silero_2", target=silero_test, kwargs=params2)
    task_file2.start()

    name_file3 = 'en_sample_2_48k.wav'
    params3 = {"filename": name_file3}
    task_file3 = threading.Thread(name="listen_silero_3", target=silero_test, kwargs=params3)
    task_file3.start()
    name_file1 = 'en_sample_1_8k.wav'
    params1 = {"filename": name_file1}
    task_file1 = threading.Thread(name="listen_vosk_1", target=get_text_from_voice, kwargs=params1)
    task_file1.start()
    name_file2 = 'en_sample_1_16k.wav'
    params2 = {"filename": name_file2}
    task_file3 = threading.Thread(name="listen_vosk_2", target=get_text_from_voice, kwargs=params2)
    task_file3.start()
    name_file3 = 'en_sample_2_48k.wav'
    params3 = {"filename": name_file3}
    task_file5 = threading.Thread(name="listen_vosk_3", target=get_text_from_voice, kwargs=params3)
    task_file5.start()


    name_file1 = 'en_sample_1_8k.wav'
    params1 = {"filename": name_file1}

    task_file6 = threading.Thread(name="listen_vosk_6", target=get_text_from_voice, kwargs=params1)
    task_file6.start()

    name_file2 = 'en_sample_1_16k.wav'
    params2 = {"filename": name_file2}

    task_file7 = threading.Thread(name="listen_vosk_7", target=get_text_from_voice, kwargs=params2)
    task_file7.start()

    name_file3 = 'en_sample_2_48k.wav'
    params3 = {"filename": name_file3}

    task_file8 = threading.Thread(name="listen_vosk_8", target=get_text_from_voice, kwargs=params3)
    task_file8.start()

    task_file9 = threading.Thread(name="listen_vosk_9", target=get_text_from_voice, kwargs=params3)
    task_file9.start()
    task_file10 = threading.Thread(name="listen_vosk_10", target=get_text_from_voice, kwargs=params3)
    task_file10.start()

    task_file11 = threading.Thread(name="listen_vosk_11", target=get_text_from_voice, kwargs=params3)
    task_file11.start()
    task_file12 = threading.Thread(name="listen_vosk_12", target=get_text_from_voice, kwargs=params3)
    task_file12.start()"""
"""    task_file2 = threading.Thread(name="listen_silero_1", target=silero_test, kwargs=params1)
    task_file2.start()
    

    task_file13 = threading.Thread(name="listen_vosk_13", target=get_text_from_voice, kwargs=params3)
    task_file13.start()
    task_file14 = threading.Thread(name="listen_vosk_14", target=get_text_from_voice, kwargs=params3)
    task_file14.start()
    
    
    task_file4 = threading.Thread(name="listen_silero_2", target=silero_test, kwargs=params2)
    task_file4.start()

    task_file6 = threading.Thread(name="listen_silero_3", target=silero_test, kwargs=params3)
    task_file6.start()"""


    #task_listen = threading.Thread(name="listen_step_1", target=va_listen)
    #task_listen.start()


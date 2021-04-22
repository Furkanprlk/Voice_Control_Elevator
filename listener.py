#!/usr/bin/env python3
import argparse
import os
import queue
import sounddevice as sd
import vosk
import sys
import json
#sys.path.append('/tmp/asansor')

q = queue.Queue()

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(indata)

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    '-f', '--filename', type=str, metavar='FILENAME',
    help='audio file to store recording to')
parser.add_argument(
    '-m', '--model', type=str, metavar='MODEL_PATH',
    help='Path to the model')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-r', '--samplerate', type=int, help='sampling rate')
args = parser.parse_args(remaining)

def listen(func):
    try:
        modelTr = vosk.Model("turkish_model")
 #       modelEng = vosk.Model("english_model")
 #       modelGer = vosk.Model("germany_model")
  #      modelRu = vosk.Model("russian_model")
   #     modelFr = vosk.Model("french_model")

        if args.model is None:
            args.model = "turkish_model"
        if not os.path.exists(args.model):
            print ("Please download a model for your language from https://alphacephei.com/vosk/models")
            print ("and unpack as 'model' in the current folder.")
            parser.exit(0)
        if args.samplerate is None:
            device_info = sd.query_devices(0, 'input')
            # soundfile expects an int, sounddevice provides a float:
            args.samplerate = int(device_info['default_samplerate'])

      
        if args.filename:
            dump_fn = open(args.filename, "wb")
        else:
            dump_fn = None

        with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=0, dtype='int16',
                                channels=1, callback=callback):
                recTr = vosk.KaldiRecognizer(modelTr, args.samplerate)
    #            recEng = vosk.KaldiRecognizer(modelEng, samplerate)
     #           recGer = vosk.KaldiRecognizer(modelGer, samplerate)
     #           recRu = vosk.KaldiRecognizer(modelRu, samplerate)
     #           recFr = vosk.KaldiRecognizer(modelFr, samplerate)
                while True:
                    data = q.get()
                    data = bytes(data)
                    if recTr.AcceptWaveform(data):
                        resultTr = json.loads(recTr.Result())["text"].split(" ")
                        print(resultTr)
                        for res in resultTr:
                            if res=="asansör":
                                func(resultTr)
    #                if recEng.AcceptWaveform(data):
    #                    resultEng = json.loads(recEng.Result())["text"].split(" ")
    #                    print(resultEng)
    #                    for res in resultEng:
    #                       if res=="hi":
    #                           func(resultEng)
    #                if recGer.AcceptWaveform(data):
    #                    resultGer = json.loads(recGer.Result())["text"].split(" ")
    #                    func(resultGer)
    #                    for res in resultGer:
    #                        if res=="aufzug":
    #                            func(resultGer)
    #                if recRu.AcceptWaveform(data):
    #                    resultRu = json.loads(recRu.Result())["text"].split(" ")
    #                    func(resultRu)
    #                    for res in resultRu:
    #                        if res=="aufzug":
    #                            func(resultRu)
    #                if recFr.AcceptWaveform(data):
    #                    resultFr = json.loads(recFr.Result())["text"].split(" ")
    #                    func(resultRu)
    #                    for res in resultFr:
    #                        if res=="aufzug":
    #                            func(resultFr)
                        
                    #else:
                    #    print(rec.PartialResult())
                    if dump_fn is not None:
                        dump_fn.write(data)

    except KeyboardInterrupt:
        print('\nDone')
        exit(0)
    except Exception as e:
        exit(type(e).__name__ + ': ' + str(e))
        

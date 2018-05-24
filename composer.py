from MIDIprocessing import *
from keras.models import load_model
import numpy as np
import pickle

def binToDec(list):
    dec = 0
    for i in list:
        dec = dec * 2 + i
    return dec


def predictY(model, n):
    Xtest = getXtest(n)
    model = load_model(model)
    data = model.predict(Xtest)
    return data

# predictY('Bandari.h5',5)

def convertOutputToMidi_(Y, file_name):
    pattern = midi.Pattern()
    track = midi.Track()
    for i in range(len_track):
        p_ = Y[i]
        p = p_.tolist()
        a = p[:8].index(max(p[:8]))
        b = p[8:].index(max(p[8:]))
        f = 24 + 12*a + b
        if f == 24:
            break
        on = midi.NoteOnEvent()
        on.tick = 10
        on.channel = 0
        on.data = [f, 100]
        off = midi.NoteOffEvent()
        off.tick = 250
        off.channel = 0
        off.data = [f, 50]
        track.append(on)
        track.append(off)
    pattern.append(track)
    midi.write_midifile(file_name, pattern)


def convertOutputToMidi(Y,YT, file_name):
    pattern = midi.Pattern()
    track = midi.Track()
    for i in range(len_track):
        p_ = Y[i]
        t_ = YT[i]
        p = p_.tolist()
        a = p[:8].index(max(p[:8]))
        b = p[8:].index(max(p[8:]))
        f = 24 + 12*a + b
        if f == 24:
            break
        t = t_.tolist()
        m = t[:5].index(max(t[:5]))
        print (t[-1])
        if t[-1] < 0.5:
            tm = int((2**m)*108)
        else:
            tm = int((2**m)*3*108/2)
        print (f, tm)
        on = midi.NoteOnEvent()
        on.tick = 10
        on.channel = 0
        on.data = [f, 100]
        off = midi.NoteOffEvent()
        off.tick = tm
        off.channel = 0
        off.data = [f, 50]
        track.append(on)
        track.append(off)
    pattern.append(track)
    midi.write_midifile(file_name, pattern)


def compose(model,modelT_, n, m):
    modelT = load_model(modelT_)
    data = predictY(model, n)
    fileName = m
    for Y in data:
        convertOutputToMidi_(Y, fileName)
        XT = convert2TXTrain(fileName)
        YT = modelT.predict(np.array([XT]))[0]
        convertOutputToMidi(Y,YT,fileName)

class Composer():
    def __init__(self,name,avatar_path,list_scr_midi = []):
        self.name = name
        self.model = 'Models/' + name + '.h5'
        self.modelt = 'Models_/' + name + '.h5'
        self.avatar = avatar_path
        self.midi = list_scr_midi
    def compose(self,filename):
        compose(self.model,self.modelt,1,'Musics/' + filename + '.mid')

#compose('TestModel/Bandari.h5','TestModel/BandariT.h5',5)

import midi
import os
import numpy as np
import random
from config import *


# MIDI DOCUMENTATION https://github.com/vishnubob/python-midi/blob/master/README.mediawiki

def readfile(file):
    f = midi.read_midifile(file)
    return f


def nomalize(srcfolder,desfolder,list_file = None):
    if list_file == None:
        list_file = os.listdir(srcfolder)
    m = 0
    for file in list_file:
        print (file)
        if list_file == None:
            f = midi.read_midifile(srcfolder + '/' + file)
        else:
            f = midi.read_midifile(file)
        l = []
        for event in f[1]:
            print(event)
            if isinstance(event, midi.NoteOnEvent) or isinstance(event, midi.NoteOffEvent):
                f_ = event.data[0]
                a = f_ % 12
                print(a)
                if a not in l:
                    l.append(a)
                if len(l) == 7:
                    break
        l.sort()
        print (l)
        pattern = midi.Pattern()
        track = midi.Track()
        for event in f[1]:
            if isinstance(event, midi.events.NoteOnEvent):
                if len(track) == 0:
                    track.append(event)
                    continue
                if isinstance(track[-1], midi.events.NoteOnEvent):
                    if event.data[0] > track[-1].data[0]:
                        track.pop()
                        track.append(event)
                    else:
                        continue
                else:
                    track.append(event)
            if isinstance(event, midi.events.NoteOffEvent):
                if isinstance(track[-1], midi.events.NoteOffEvent):
                    if event.data[0] > track[-1].data[0]:
                        track.pop()
                        track.append(event)
                    else:
                        continue
                else:
                    track.append(event)
            if len(track) < max_note + 2:
                continue
            if isinstance(track[-1], midi.events.NoteOnEvent) and isinstance(track[-2], midi.events.NoteOffEvent) and \
                            track[-2].tick >= 1296:
                a = track.pop()
                pattern.append(track)
                midi.write_midifile(desfolder + '/' + str(m) + '.mid', pattern)
                pattern = midi.Pattern()
                track = midi.Track()
                track.append(a)
                m = m + 1
            elif isinstance(track[-1], midi.events.NoteOffEvent) and isinstance(track[-2], midi.events.NoteOnEvent) and \
                            track[-2].tick >= 192:
                a = track.pop()
                b = track.pop()
                pattern.append(track)
                midi.write_midifile(desfolder + '/' + str(m) + '.mid', pattern)
                pattern = midi.Pattern()
                track = midi.Track()
                track.append(b)
                track.append(a)
                m = m + 1

        pattern.append(track)
        midi.write_midifile(desfolder + '/' + str(m) + '.mid', pattern)


def convertToSheet(file):
    data = readfile(file)
    sheet = []
    for event in data[0]:
        if isinstance(event, midi.events.NoteOnEvent):
            node = {'f': event.data[0]}

        if isinstance(event, midi.events.NoteOffEvent):
            node['t'] = event.tick
            sheet.append([node])
    return sheet


def convertToYTrain_(file):
    sheet = convertToSheet(file)
    if len(sheet) > len_track:
        return None
    if len(sheet) <= min_track:
        return None
    data = []
    for p in sheet:
        b = p[0]['f'] % 12
        a = int((p[0]['f'] - b) / 12 - 2)
        if a > 8 or a < 0:
            return None
        l = [0 for i in range(20)]
        l[a] = 1
        l[b + 8] = 1
        data.append(l)
    while len(data) < len_track:
        t = [0 for i in range(20)]
        t[0] = 1
        t[8] = 1
        data.append(t)
    if len(sheet) < len_track:
        return np.array(data), len(sheet)
    else:
        return np.array(data), len_track


def getXTrain(n):
    Xtrain = []
    for i in range(n):
        Xtrain.append(random.randint(1, 255))
    while (len(Xtrain) < len_track):
        Xtrain.append(0)
    return np.array(Xtrain)


def getTrainingData(folder, n):
    list_file = os.listdir(folder)
    dataX = []
    dataY = []
    for file in list_file:
        print (file)
        data = convertToYTrain_(folder + '/' + file)
        if data == None:
            continue
        else:
            Y, numOfEvent = data
        for i in range(n):
            dataY.append(Y)
            dataX.append(getXTrain(numOfEvent))
    return np.array(dataX), np.array(dataY)


def getXtest(n):
    Xtest = []
    for j in range(n):
        r = 0
        while r > len_track or r < 5:
            r = int(np.random.normal(350, 50, 1)[0])
        X = []
        for i in range(r):
            X.append(random.randint(0, 255))
        for i in range(len_track - r):
            X.append(0)
        Xtest.append(X)
    return np.array(Xtest)

# print getXtest(5).shape

def loadTrainingData(x, y):
    X = np.load(x + '.npy')
    Y = np.load(y + '.npy')
    return X, Y


def generateTrainingData(midiFolder, n, Xfile, Yfile):
    X, Y = getTrainingData(midiFolder, n)
    print (X.shape)
    print (Y.shape)
    np.save(Xfile, X)
    np.save(Yfile, Y)


def readAndPlay(file):
    f = readfile(file)
    m = 0
    for event in f[0]:
        print (m, event)
        m += 1
    os.system('timidity ' + file)


def modify(file, l):
    pattern = midi.Pattern()
    f = readfile(file)[0]
    l.sort()
    l.reverse()
    print (l)
    for i in l:
        f.pop(i)
    pattern.append(f)
    midi.write_midifile(file[:-4] + '.mid', pattern)


def listToMidi(listp, file):
    pattern = midi.Pattern()
    track = midi.Track()
    for i in listp:
        f = i[0]['f']
        on = midi.NoteOnEvent()
        on.tick = 0
        on.channel = 0
        on.data = [f, 100]
        off = midi.NoteOffEvent()
        off.tick = i[0]['t']
        off.channel = 0
        off.data = [f, 50]
        track.append(on)
        track.append(off)
    pattern.append(track)
    midi.write_midifile(file, pattern)

def getTTrainingY(file):
    p = convertToSheet(file)
    l = []
    for i in p:
        a = i[0]['t']
        if a < 150:
            l.append([1, 0, 0, 0, 0, 0])
        elif a >= 150 and a < 215:
            l.append([1, 0, 0, 0, 0, 1])
        elif a >=215 and a < 324:
            l.append([0, 1, 0, 0, 0, 0])
        elif a >= 324 and a < 420:
            l.append([0, 1, 0, 0, 0, 1])
        elif a >=420 and a < 640:
            l.append([0, 0, 1, 0, 0, 0])
        elif a >=620 and a < 820:
            l.append([0, 0, 1, 0, 0, 1])
        elif a >=820 and a < 1200:
            l.append([0, 0, 0, 1, 0, 0])
        elif a >= 1200 and a < 1680:
            l.append([0, 0, 0, 1, 0, 1])
        elif a >=1680 and a < 2500:
            l.append([0, 0, 0, 0, 1, 0])
        elif a >=2500:
            l.append([0, 0, 0, 0, 1, 1])
        else:
            print ('_________________ ERROR __________________')
    while (len(l) < len_track):
        l.append([0, 0, 0, 0, 0, 0])
    if len(l) > len_track:
        l = l[:len_track]
    return np.array(l)


def convert2TXTrain(file):
    sheet = convertToSheet(file)
    data = []
    for p in sheet:
        b = p[0]['f'] % 12
        a = int((p[0]['f'] - b) / 12 - 2)
        if a > 8 or a < 0:
            return None
        l = [0 for i in range(20)]
        l[a] = 1
        l[b + 8] = 1
        l.append(random.random())
        l.append(random.random())
        data.append(l)
    while len(data) < len_track:
        t = [0 for i in range(20)]
        t[0] = 1
        t[8] = 1
        t.append(random.random())
        t.append(random.random())
        data.append(t)
    if len(data) > len_track:
        data = data[:len_track]
    return np.array(data)


# x = convert2TXTrain('BandariTrainingSet/SnowDream1.mid')
# for i in x:
#     print i



def getTTrainingData(folder, n):
    lf = os.listdir(folder)
    X = []
    Y = []
    for file in lf:
        y = getTTrainingY(folder + '/' + file)
        for i in range(n):
            x = convert2TXTrain(folder + '/' + file)
            X.append(x)
            Y.append(y)
    return np.array(X), np.array(Y)

def generateTTrainingData(midiFolder, n, Xfile, Yfile):
    X, Y = getTTrainingData(midiFolder, n)
    print (X.shape)
    print (Y.shape)
    np.save(Xfile, X)
    np.save(Yfile, Y)
# nomalize('Bandari', 'Bandari_')
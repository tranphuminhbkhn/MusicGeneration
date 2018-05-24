from keras.models import Sequential
from keras.layers import Dense
from keras.layers import TimeDistributed
from keras.layers import Embedding
from keras.layers import LSTM
from keras.models import load_model
from config import *
from MIDIprocessing import loadTrainingData

# random.seed(19)
def generateModel(name,n):
    model = Sequential()
    model.add(Embedding(256, 20, input_length=len_track))
    model.add(LSTM(n, return_sequences=True))
    model.add(LSTM(n, return_sequences=True))
    model.add(TimeDistributed(Dense(20,activation='sigmoid')))
    model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
    print(model.summary())
    model.save(name)

def generateTModel(name,n):
    model = Sequential()
    model.add(LSTM(n, return_sequences=True, input_shape=(len_track,22)))
    model.add(LSTM(n, return_sequences=True))
    model.add(TimeDistributed(Dense(6,activation='sigmoid')))
    model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
    print(model.summary())
    model.save(name)

def trainModel(model_,Xfile,Yfile,time,epochs):
    for i in range(time):
        model = load_model(model_)
        X, Y = loadTrainingData(Xfile, Yfile)
        print(model.summary())
        model.fit(X, Y, epochs=epochs, batch_size=600)
        model.save(model_)

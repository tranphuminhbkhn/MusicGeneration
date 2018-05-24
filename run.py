from MIDIprocessing import *
from model import *
from composer import *
def init():
    # generateTrainingData('BandariTrainingSet',100,'X', 'Y')
    # generateTTrainingData('BandariTrainingSet',50,'XT', 'YT')
    generateModel('TestModel/Yiruma', 60)
    generateTModel('TestModel/YirumaT', 30)
def train():
    for i in range(1000):
        trainModel('TestModel/Yiruma', 'X', 'Y', 2, 10)
        #trainModel('TestModel/YirumaT','XT', 'YT', 5, 20)
if __name__ == '__main__':
    init()
    #train()

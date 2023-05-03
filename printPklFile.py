#pass this a pkl file name, and it will convert it to spikes.
import sys
import cPickle as pickle
import glob

def printPklSpikes(folder):
        files = glob.glob(folder+"/*/*.pkl")
        for fileName in files:
            print(fileName)
            fileHandle = open(fileName)
            neoObj = pickle.load(fileHandle)        
            segments = neoObj.segments
            segment = segments[0]
            spikeTrains = segment.spiketrains
            neurons = len(spikeTrains)
            for neuronNum in range (0,neurons):
                if (len(spikeTrains[neuronNum])>0):
                    spikes = spikeTrains[neuronNum]
                    for spike in range (0,len(spikes)):
                        print(neuronNum, spikes[spike])
            fileHandle.close()


#--main
args = sys.argv
numberArgs = args.__len__()
if (numberArgs == 2):
    folder = args[1]
else:
    folder = "pkls"

printPklSpikes(folder)
    

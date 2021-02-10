"""
    Name: Aseem Thapa
    ID: 1001543178
"""
import numpy as np 
import matplotlib.pyplot as plt
import soundfile as sf #soundfile to extract audio to array
from scipy.signal import spectrogram
import glob


# This function creates signature for each of database's songs
def createSignature(f,t,Sxx):
    y = np.zeros(len(t))
    colarr = np.zeros(len(f))    
    for i in range(0,len(t)):
        for j in range(0,len(f)):
            colarr[j] = Sxx[j][i]
        ind = findMaxIndex(colarr)
        y[i] = f[ind]
    return y  

#Function to find maximum in an array:
def findMaxIndex(arr):
    max = -np.inf
    ind = 0
    for i in range(0,len(arr)):
        if(arr[i]>max):
            max = arr[i]
            ind = i
    return ind

 
#Function to calculate 1-norm    
def calculateOneNorm(arr):
    OneNorm = 0
    for i in range(0,len(arr)):
        OneNorm  += np.abs(arr[i])
    return OneNorm
        
def classifyMusic() :
    """LIST OF FILES TO OPEN"""
    #Audio Files to be checked has to be form: song-*.wav
    fileList = glob.glob('song-*.wav')
    
    y = []
    
    """CREATE THE SIGNATURES FOR SONGS"""
    for n in range (0,np.size(fileList)):
        #OPEN AND READ FILES---------->
        x, fs = sf.read(fileList[n])
        """x is the audio array and fs is the sampling frequency"""     
        #SPECTOGRAM:
        f, t, Sxx = spectrogram(x, fs=fs, nperseg=fs//2)
        y.append(createSignature(f,t,Sxx))
      
    """    
    #Test Case---------->
    #OPEN AND READ FILES---------->
    x, fs = sf.read('song-beatles.wav')
    #SPECTOGRAM:
    f, t, Sxx = spectrogram(x, fs=fs, nperseg=fs//2)
    y = createSignature(f,t,Sxx)
    print(y)
    """
    
    #INPUT FILE sample name: 'testSong.wav'-------------->
    testFile = 'testSong.wav'
    x,fs = sf.read(testFile)
    f, t, Sxx = spectrogram(x, fs=fs, nperseg=fs//2)
    yout = createSignature(f,t,Sxx)
    
    
    """CALCULATE 1-Norm"""
    oneNormVector = np.zeros(np.size(fileList))
    
    """Create one norm vector that stores one norm for each test song"""
    for n in range (0,np.size(fileList)):
        oneNormVector[n] = calculateOneNorm(y[n]-yout)
    
    #print(oneNormVector)
    
    """CALCULATE FIVE Minimum INDICES"""
    indices = np.zeros(5)  
    indices = oneNormVector.argsort()[:5]
    
    #print(indices[0])
    """PRINT THE OUTPUT"""
    for i in range (0,len(indices)):
        print(int(oneNormVector[indices[i]]),fileList[indices[i]])
    
    """PLOT--------->"""
    x1, fs1 = sf.read(fileList[indices[0]])
    x2, fs2 = sf.read(fileList[indices[1]])
    x,fs = sf.read(testFile)
    plt.specgram(x, Fs=fs)
    plt.show()
    plt.specgram(x1, Fs=fs1)
    plt.show()
    plt.specgram(x2, Fs=fs2)
    plt.show()
    pass


###################  main  ###################
if __name__ == "__main__" :
    classifyMusic()

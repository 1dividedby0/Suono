import matplotlib.pyplot as plt
import scipy.io.wavfile
from scipy.fftpack import fft
import numpy as np
rate, amp_arr = scipy.io.wavfile.read('IbizaHum.wav')
print rate
hum_rate, hum_amp = scipy.io.wavfile.read('IbizaHum.wav')
fft_out = fft(amp_arr)
fft_out_hum = fft(hum_amp)
average = 0
averages = []
averages_hum = []
#peaks = []
index = 0
tension = 20
for i in range(64000):
    print i
#for i in np.abs(fft_out):
#    average += i[0]
#    index+=1
#    if index%(rate/tension) == 0:
#        averages.append(average/(rate/tension))
##        #print average/40000
#        average = 0
#average = 0
#for i in np.abs(fft_out_hum):
#    average += i[0]
#    index+=1
#    if index%(rate/tension) == 0:
#        averages_hum.append(average/(rate/tension))
##        #print average/40000
#        average = 0
#print averages
#print averages_hum
#similarity_scores = []
#print len(averages)
#print len(averages_hum)
#for j in range(len(averages)-len(averages_hum)):
#    start = j
#    end = j+len(averages_hum)
#    averages_frame = averages[start:end]
#    similarity_score = 0
#    for i in range(len(averages_hum)-1):
#        #print str(np.abs(averages[i])) + " " + str(np.abs(averages_hum[i]))
#        if (np.abs(averages_frame[i]) > np.abs(averages_frame[i+1]) and np.abs(averages_hum[i]) > np.abs(averages_hum[i+1])) or (np.abs(averages_frame[i]) <  np.abs(averages_frame[i+1]) and np.abs(averages_hum[i]) < np.abs(averages_hum[i+1])):
#            similarity_score += 1
#    similarity_score = similarity_score/(len(averages_hum)*1.0)
#    similarity_scores.append(similarity_score)
#    print similarity_score
#print max(similarity_scores)







    

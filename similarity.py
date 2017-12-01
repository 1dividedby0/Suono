import matplotlib.pyplot as plt
import scipy.io.wavfile
from scipy.fftpack import fft
import numpy as np

file_1 = 'IbizaHum.wav'
file_2 = 'TookAPillInIbizaSong.wav'
rate, amp_arr = scipy.io.wavfile.read(file_2)
hum_rate, hum_amp = scipy.io.wavfile.read(file_1)
print rate
print hum_rate
fft_out = fft(amp_arr)
fft_out_hum = fft(hum_amp)
index = 0

#ALWAYS FORMAT AS 16-bit PCM: -32768,+32767:int16 output
#65536: divide by 32768 for position out of [-1, 1)
def average(list):
    averages = []
    average = 0
    tension = rate/8
    index = 0
    for i in np.abs(list):
        average += i[0]
        index+=1
        if index%tension == 0:
            averages.append(average/tension)
#           print average/40000
            average = 0
    return averages

def howManyElementsAreZeroAfterThisIndex(array, index):
    num = 0
    if index == len(array) or index+1 == len(array):
        return 0
    while(array[index+1] == 0):
        index+=1
        num+=1
        if index+1 == len(array):
            break
    return num

def mono(amps, file):
    f = open(file.replace('wav', 'txt'), "w")
    hunnidtracker=0
    counter=0 
    mono_arr = []
    zero_arr=[]
    amp_clusters = []
    for j in amps:
        if hunnidtracker == 2000:
            zero_arr.append(counter)
            print counter
            counter=0
            hunnidtracker = 0
        #Float range from -1 to 1 for amplitude
        temp = (j[0]/2 + j[1]/2)/32678.0
        if temp > 0.25 or temp < -0.25:
            mono_arr.append(0)
            counter+=1
        else:
            mono_arr.append((j[0]/2 + j[1]/2)/32678.0)
        hunnidtracker+=1
    cluster_start = 0
    cluster_end = 0
    i = 0
    print "zero_arr len: ",len(zero_arr), " ", len(amps)
    while i < len(zero_arr):
        numElementsZero = howManyElementsAreZeroAfterThisIndex(zero_arr, i)
        #print i," : ", numElementsZero, " : cluster start : ", cluster_start, ", cluster end : ", cluster_end
        if numElementsZero < 8:
            cluster_end+=1
            i+=1
        elif cluster_start != cluster_end and cluster_start + 1 != cluster_end:
            amp_clusters.append(((cluster_start+1)*2000, cluster_end*2000))
            std = str((cluster_start+1)*2000) + "," + str(cluster_end*2000) + "\n"
            f.write(std)
            cluster_start = cluster_end+numElementsZero
            cluster_end = cluster_start
            i+=numElementsZero
        else:
            cluster_start = cluster_end+numElementsZero
            cluster_end = cluster_start
            i+=numElementsZero
    if cluster_start != cluster_end and cluster_start + 1 != cluster_end:
        amp_clusters.append(((cluster_start+1)*2000, cluster_end*2000))
        print ((cluster_start+1)*2000, cluster_end*2000)
        std = str((cluster_start+1)*2000) + "," + str(cluster_end*2000) + "\n"
        f.write(std)
    f.close()
    return amp_clusters
        
def similarity(averages_1, averages_2):
    similarity_score = 0
    for i in range(len(averages_2)-1):
        #print str(np.abs(averages[i])) + " " + str(np.abs(averages_hum[i]))
        if (np.abs(averages_1[i]) > np.abs(averages_1[i+1]) and np.abs(averages_2[i]) > np.abs(averages_2[i+1])) or (np.abs(averages_1[i]) < np.abs(averages_1[i+1]) and np.abs(averages_2[i]) < np.abs(averages_2[i+1])):
            similarity_score += 1
    similarity_score = similarity_score/(len(averages_2)*1.0)
    return similarity_score

#amp_clusters = mono(amp_arr, file_2)
amp_clusters_hum = mono(hum_amp, file_1)
print "hum: ", amp_clusters_hum
similarities = []
#f = open("first_cluster_ibiza.txt", 'w')
#f1 = open("first_cluster_ibiza_hum.txt", 'w')
#print "fft_out"
#for m in average(fft_out[amp_clusters[0][0]:amp_clusters[0][1]]):
#    l = str(m) + "\n"
#    f.write(l)
#print "fft_out_hum"
#for n in average(fft_out_hum[amp_clusters_hum[0][0]:amp_clusters_hum[0][1]]):
#    l = str(n) + "\n"
#    f1.write(l)

amp_clusters = []
txt_song = open(file_2.replace('wav', 'txt'))
for line in txt_song:
    contents = line.split(',')
    contents[0] = int(contents[0])
    contents[1] = int(contents[1])
    amp_clusters.append((contents[0], contents[1]))
print amp_clusters

found = 0
for d in range(len(amp_clusters) - len(amp_clusters_hum)):
    passed = True
    for e in range(len(amp_clusters_hum)):
        score = np.abs((amp_clusters[d+e][1] - amp_clusters[d+e][0]) - (amp_clusters_hum[e][1] - amp_clusters_hum[e][0]))
        if score > 20000:
            # did not pass
            passed = False
    if passed:
        found += 1
print "Found: ", found
#        
#for k in amp_clusters_hum:
#    for l in amp_clusters:
#        averages_1 = average(fft_out[l[0]:l[1]])
#        averages_2 = average(fft_out_hum[k[0]:k[1]])
#        if len(averages_1) < len(averages_2):
#            temp = averages_2
#            averages_2 = averages_1
#            averages_1 = temp
#        print len(amp_clusters_hum)
#        print len(amp_clusters)
#        if k[0] == k[1] or l[0] == l[1]:
#            continue
#        similarity_score = similarity(averages_1, averages_2)
#        print k, ", ", l, " : ", similarity_score
#        similarities.append(similarity_score)
#
#print max(similarities)

#for i in range(len(zero_arr)):
    #print mono_arr[i]
    #print i
    #print i*2000,": ",zero_arr[i]

# #for i in np.abs(fft_out):
#     average += i[0]
#     index+=1
#     if index%(rate/10000) == 0:
#         averages.append(average/(rate/10000))
#     #print average/40000
#     average = 0
# #average = 0
# #for i in np.abs(fft_out_hum):
#     # average += i[0]
#     index+=1
#     if index%(rate/10000) == 0:
#         fft_out_hum.append(average/(rate/10000))
# #        #print average/40000
#         average = 0

#Loop through and check similarity
# for j in range(len(fft_out)-len(fft_out_hum)):
#     start = j
#     end = j+len(fft_out_hum)
#     fft_out_frame = fft_out[start:end]
#     similarity_score = 0
#     for i in range(len(fft_out_hum)-1):
#         #print str(np.abs(averages[i])) + " " + str(np.abs(fft_out_hum[i]))
#         if (np.abs(fft_out_frame[i][0]) > np.abs(fft_out_frame[i+1][0]) and np.abs(fft_out_hum[i][0]) > np.abs(fft_out_hum[i+1][0])) or (np.abs(fft_out_frame[i][0]) <  np.abs(fft_out_frame[i+1][0]) and np.abs(fft_out_hum[i][0]) < np.abs(fft_out_hum[i+1][0])):
#             similarity_score += 1
#     print similarity_score/(len(fft_out_hum)*1.0)

#amplitude grouping
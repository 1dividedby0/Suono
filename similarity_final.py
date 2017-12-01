import scipy.io.wavfile
import numpy as np
import boto

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

def mono(amps):
    hunnidtracker=0
    counter=0 
    mono_arr = []
    zero_arr=[]
    amp_clusters = []
    for j in amps:
        if hunnidtracker == 2000:
            zero_arr.append(counter)
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
    while i < len(zero_arr):
        numElementsZero = howManyElementsAreZeroAfterThisIndex(zero_arr, i)
        if numElementsZero < 8:
            cluster_end+=1
            i+=1
        elif cluster_start != cluster_end and cluster_start + 1 != cluster_end:
            amp_clusters.append(((cluster_start+1)*2000, cluster_end*2000))
            std = str((cluster_start+1)*2000) + "," + str(cluster_end*2000) + "\n"
            cluster_start = cluster_end+numElementsZero
            cluster_end = cluster_start
            i+=numElementsZero
        else:
            cluster_start = cluster_end+numElementsZero
            cluster_end = cluster_start
            i+=numElementsZero
    if cluster_start != cluster_end and cluster_start + 1 != cluster_end:
        amp_clusters.append(((cluster_start+1)*2000, cluster_end*2000))
        std = str((cluster_start+1)*2000) + "," + str(cluster_end*2000) + "\n"
    return amp_clusters

def similarity(txt_song_name, wav_hum_name):
    hum_rate, hum_amp = scipy.io.wavfile.read(wav_hum_name)
    amp_clusters_hum = mono(hum_amp)
    print "hum: ", amp_clusters_hum

    amp_clusters = []
    txt_song = open(txt_song_name)
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
    return found

def suono(wav_hum_name):
    names = []
    conn = boto.connect_s3(anon=True)
    bucket = conn.get_bucket('suono-textfiles')
    for key in bucket.list():
        names.append(key.name.encode('utf-8'))
    highest = 0
    highest_file = ''
    for f in names:
        similarity_score = similarity(f, wav_hum_name)
        if similarity_score > highest:
            highest = similarity_score
            highest_file = f
    return highest_file

def handler(event, context):
    return suono(event['hum_file'])

print suono('IbizaHum.wav')
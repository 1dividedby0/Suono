import scipy.io.wavfile
file_name = 'SweaterWeatherSong.wav'
rate, amp_arr = scipy.io.wavfile.read(file_name)

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

def mono(amps, file_name):
    f = open(file_name.replace('wav', 'txt'), "w")
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

print mono(amp_arr, file_name)
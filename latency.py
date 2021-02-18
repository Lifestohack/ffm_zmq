import csv
import matplotlib.pyplot as plt
import numpy as np

def histogram(listfps):
    # An "interface" to matplotlib.axes.Axes.hist() method
    n, bins, patches = plt.hist(x=listfps, bins='auto', color='#0504aa',
                                alpha=0.7, rwidth=0.85)
    plt.grid(axis='y', alpha=0.75)
    plt.ylabel('seconds')
    plt.xlabel('sampling frequency')
    #plt.title('My Very Own Histogram')
    plt.text(23, 45, r'$\mu=15, b=3$')
    maxfreq = n.max()
    # Set a clean upper y-axis limit.
    plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
    plt.savefig('histogram.png')
    plt.show()

def readcsv():
    data = []
    with open("lat192.csv", newline="",) as f:
        reader = csv.DictReader(f)        
        for row in reader:
            data.append(row)
    return data
data = readcsv()

image_exposure_latency = []
image_network_read_latency = []
fps = 0
fps_list = []
first_read_time = float(data[0]['exposure_start'])
read_time = float(data[0]['exposure_start'])
end_time = float(data[-1]['exposure_end'])
for row in data:
    curr_time = float(row['exposure_start'])
    if (curr_time - read_time) >= 1:
        print(fps)
        fps_list.append(fps)
        read_time = float(row['exposure_start'])
        fps = 0
    fps += 1
    image_read_latency = float(row['exposure_end']) - float(row['exposure_start'])
    image_client_read_latency = float(row['client_end']) - float(row['client_start'])
    #total_latency = image_read_latency * 1000 + image_client_read_latency * 1000 + 1 # 1ms as the network latency
    image_exposure_latency.append(image_read_latency)
    image_network_read_latency.append(image_client_read_latency)
    #print("Frame:" + row["index"])

avg_exposure = sum(image_exposure_latency)/len(image_exposure_latency) * 1000
avg_client = sum(image_network_read_latency)/len(image_network_read_latency) *  1000
print("Average exposure time:" + str(avg_exposure))
print("Average client read time from network:" + str(avg_client))
print("Total required time from begining of exposure till client read time:" + str(avg_exposure + avg_client + 1)) # 1ms network latency
print("Total sample time:" + str(end_time - first_read_time) + "seconds." )
histogram(fps_list)
pass
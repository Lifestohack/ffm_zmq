import zmq
from zmq_tools import Msg_Receiver, Msg_Streamer
import cv2
from time import time
import numpy as np
import sys
import ffmpeg
import io
from threading import Thread
import subprocess
import traceback
import sys
import helper
import csv
import matplotlib.pyplot as plt

host = "10.3.141.1"
port = "50020"

ctx = zmq.Context()
icp_req_add = "tcp://{}:{}".format(host, port)
msg_receiver = Msg_Receiver(
    ctx, icp_req_add, topics=("hmd_streaming.world",), block_until_connected=False
)

def export(listtocsv):
    with open("lat.csv", "w", newline="") as csvfile:
        fieldnames = ["index", "exposure_start", "exposure_end", "client_start","client_end"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(listtocsv)

def histogram(listfps):

    # An "interface" to matplotlib.axes.Axes.hist() method
    n, bins, patches = plt.hist(x=listfps, bins='auto', color='#0504aa',
                                alpha=0.7, rwidth=0.85)
    #plt.grid(axis='y', alpha=0.75)
    #plt.xlabel('Value')
    #plt.ylabel('Frequency')
    #plt.title('My Very Own Histogram')
    #plt.text(23, 45, r'$\mu=15, b=3$')
    #maxfreq = n.max()
    # Set a clean upper y-axis limit.
    #plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
    plt.show()


try:
    frame = 1
    fps = 0
    index = 0
    start_time = time()
    l_start_time = time()
    output = []
    fpslisthistogram = []
    for i in range(20000):
        temp = {}
        topic, payload = msg_receiver.recv()
        received = time()
        #size = sys.getsizeof(payload["__raw_data__"][0])
        latency = time() - l_start_time
        #image = helper.YUVtoBGR(
        #    payload["__raw_data__"][0], payload["width"], payload["height"]
        #)
        image = np.frombuffer(payload["__raw_data__"][0], np.uint8).reshape([payload["height"], payload["width"]])
        #cv2.imshow("frame", image)
        #if cv2.waitKey(1) & 0xFF == ord("q"):
        #    break
        if time() - start_time > 1:
            fps = frame
            frame = 0
            start_time = time()
            fpslisthistogram.append(fps)
        outstr = "Frames: {}, FPS: {}, Latency: {:.6f}".format(index, fps, latency)
        sys.stdout.write("\r" + outstr)
        frame = frame + 1
        index = index + 1
        temp["index"] = payload["index"]
        temp["exposure_start"] = payload["timestamp"]
        temp["exposure_end"] = payload["end_timestamp"]
        temp["client_start"] = l_start_time
        temp["client_end"] = received
        output.append(temp)
        l_start_time = time()
    #export(output)
    #histogram(fpslisthistogram)

except (KeyboardInterrupt, SystemExit):
    print("KeyboardInterrupt")
except Exception as ex:
    print("Exception")
    print(ex)
finally:
    print("finally")
    cv2.destroyAllWindows()

import ffm
from time import time, sleep
import sys
from zmq_tools import Msg_Streamer
import zmq
from payload import Payload
import numpy as np
import logging as logger
import traceback

# import cv2

host = "10.3.141.1"
port = "12349"
ctx = zmq.Context()
icp_req_add = "tcp://{}:{}".format(host, port)
msg_streamer = Msg_Streamer(ctx, icp_req_add)

source = "/dev/video0"
cap = ffm.VideoCapture(source, pix_fmt="yuv420p")

width = 320
height = 240
frame = 1
fps = 0
index = 0
cap.setResolution(width, height)
cap.start()
payload = Payload("world", width, height, format="yuv")
image = cap.read()
width = image.shape[1]
height = image.shape[0]
start_time = image_read_time = time()
try:
    while True:
        image = cap.grab()
        latency = time() - image_read_time
        payload.setPayloadParam(time(), image, index)
        msg_streamer.send(payload.get())
        if time() - start_time > 1:
            fps = frame
            frame = 0
            start_time = time()
        outstr = "Frames: {}, FPS: {}, Frame Read latency: {:.6f} ".format(
            index, fps, latency
        )
        sys.stdout.write("\r" + outstr)
        frame = frame + 1
        index = index + 1
        image_read_time = time()
except Exception:
    exp = traceback.format_exc()
    print(exp)
finally:
    cap.release()

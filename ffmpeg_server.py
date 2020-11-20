from frame import Ffmpegdata
from time import time, sleep
import sys
from zmq_tools import Msg_Streamer
import zmq
from payload import Payload
import ffmpeg as f
import numpy as np

host = "192.168.0.213"
port = "55555"
ctx = zmq.Context()
pupil_remote = zmq.Socket(ctx, zmq.REQ)
icp_req_add = "tcp://{}:{}".format(host, port)
msg_streamer = Msg_Streamer(ctx, icp_req_add)

ffmpeg = Ffmpegdata()

width = 640
height = 480
payload = Payload("world", width, height)
frame = 1
fps = 0
index = 0
start_time = time()

while True:
    image = ffmpeg.get()
    out = np.frombuffer(image)
    payload.setPayloadParam(time(), image, index)
    msg_streamer.send(payload.get())
    if time() - start_time > 1:
        fps = frame
        frame = 0
        start_time = time()
    outstr = "Frames: {}, FPS: {}    ".format(index, fps) 
    sys.stdout.write('\r'+ outstr)
    frame = frame + 1
    index = index + 1
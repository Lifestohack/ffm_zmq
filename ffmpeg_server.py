from frame import Ffmpegdata
from time import time, sleep
import sys
from zmq_tools import Msg_Streamer
import zmq
from payload import Payload
import ffmpeg as f
import numpy as np
import logging as logger

host = "127.0.0.1"
port = "50020"
ctx = zmq.Context()
pupil_remote = zmq.Socket(ctx, zmq.REQ)
icp_req_add = "tcp://{}:{}".format(host, port)
msg_streamer = Msg_Streamer(ctx, icp_req_add)

source = "/dev/video0"
ffmpeg = Ffmpegdata(source)

width = 640
height = 360
payload = Payload("world", width, height)
frame = 1
fps = 0
index = 0
start_time = time()
frame = ffmpeg.read()
if frame is None:
    logger.critical('End of input stream')
while True:
    image = ffmpeg.read()
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
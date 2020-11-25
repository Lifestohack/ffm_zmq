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

host = "10.3.141.1"
port = "12349"

ctx = zmq.Context()
icp_req_add = "tcp://{}:{}".format(host, port)
msg_receiver = Msg_Receiver(ctx, icp_req_add, topics=("hmd_streaming.world",), block_until_connected=False)

try:
    frame = 1
    fps = 0
    index = 0
    start_time = time()
    l_start_time = time()
    while True:
        topic, payload = msg_receiver.recv()
        size = sys.getsizeof(payload['__raw_data__'][0])
        latency = time() - l_start_time
        image = helper.YUVtoBGR(payload['__raw_data__'][0], payload['width'], payload['height'])
        cv2.imshow('frame', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if time() - start_time > 1:
            fps = frame
            frame = 0
            start_time = time()
        outstr = "Frames: {}, FPS: {}, Latency: {:.6f}".format(index, fps, latency) 
        sys.stdout.write('\r'+ outstr)
        frame = frame + 1
        index = index + 1
        l_start_time = time()

except (KeyboardInterrupt, SystemExit):
    print("KeyboardInterrupt")
except Exception as ex:
    print("Exception")
    print(ex)
finally:
    print("finally")
    cv2.destroyAllWindows()
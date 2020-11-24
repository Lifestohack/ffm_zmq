import zmq
from zmq_tools import Msg_Receiver, Msg_Streamer
import cv2
from time import time
import numpy as np
import sys

host = "127.0.0.1"
port = "50020"

ctx = zmq.Context()
pupil_remote = zmq.Socket(ctx, zmq.REQ)
icp_req_add = "tcp://{}:{}".format(host, port)
msg_receiver = Msg_Receiver(ctx, icp_req_add, topics=("hmd_streaming.world",), block_until_connected=False, hwm=1)

try:
    frame = 1
    fps = 0
    index = 0
    start_time = time()
    while True:
        topic, payload = msg_receiver.recv()
        latency = time() - payload["timestamp"]
        image = np.frombuffer(payload['__raw_data__'][0], dtype=np.uint8).reshape(payload['height'], payload['width'], 3)
        cv2.imshow('frame', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if time() - start_time > 1:
            fps = frame
            frame = 0
            start_time = time()
        outstr = "Frames: {}, FPS: {}, Latency: {}".format(payload["index"], fps, latency) 
        sys.stdout.write('\r'+ outstr)
        frame = frame + 1
        index = index + 1
except (KeyboardInterrupt, SystemExit):
    print("KeyboardInterrupt")
except Exception as ex:
    print("Exception")
    print(ex)
finally:
    print("finally")
    cv2.destroyAllWindows()
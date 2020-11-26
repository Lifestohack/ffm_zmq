import zmq
from zmq_tools import Msg_Receiver, Msg_Streamer
import cv2
from payload import Payload
from time import time
import sys

host = "192.168.0.188"
port = "55555"

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 420)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 340)
cap.set(cv2.CAP_PROP_FPS, 32)

ctx = zmq.Context()
pupil_remote = zmq.Socket(ctx, zmq.REQ)
icp_req_add = "tcp://{}:{}".format(host, port)
msg_streamer = Msg_Streamer(ctx, icp_req_add)

_, frame = cap.read()
if not _:
    print("Can't receive frame (stream end?). Exiting ...")
    exit()
width = frame.shape[1]
height = frame.shape[0]
payload = Payload("world", width, height)

try:
    frame = 1
    fps = 0
    index = 0
    start_time = time()
    while True:
        ret, image = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        payload.setPayloadParam(time(), image, index)
        msg_streamer.send(payload.get())
        if time() - start_time > 1:
            fps = frame
            frame = 0
            start_time = time()
        outstr = "Frames: {}, FPS: {}".format(index, fps)
        sys.stdout.write("\r" + outstr)
        frame = frame + 1
        index = index + 1
except (KeyboardInterrupt, SystemExit):
    print("KeyboardInterrupt")
except Exception:
    print("Exception")
finally:
    cap.release()
    print("finally")

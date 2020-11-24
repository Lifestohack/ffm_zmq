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

host = "10.3.141.1"
port = "12349"

ctx = zmq.Context()
icp_req_add = "tcp://{}:{}".format(host, port)
msg_receiver = Msg_Receiver(ctx, icp_req_add, topics=("hmd_streaming.world",), block_until_connected=False, hwm=1)

width = 320
height = 240

# arg = (
#     ffmpeg
#     .input('pipe:',
#         loglevel='quiet',
#         format='h264', 
#         )
#     .output('pipe:', 
#             format='rawvideo', 
#             pix_fmt='rgb24',
#             s=f'{width}x{height}')
#     .compile()
# )
# process = subprocess.Popen(arg, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

# def decode():
#     in_bytes = process.stdout.read(width * height * 3)
#     in_frame = (
#         np
#         .frombuffer(in_bytes, np.uint8)
#         .reshape([height, width, 3])
#     )
#     return in_frame


# def run():
#     try:
#         while True:
#             _, payload = msg_receiver.recv()
#             in_bytes = payload['__raw_data__'][0]
#             process.stdin.write(in_bytes)
#     except (KeyboardInterrupt, SystemExit):
#         print("KeyboardInterrupt")
#     except Exception:
#         print("Exception")
#         exp = traceback.format_exc()
#         print(exp)
#     finally:
#         print("finally")

# t1 = Thread(target=run, args=[])
# t1.start()

# while True:
#     image = decode()
#     cv2.imshow('frame', image)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

def convertYUVtoRGB2(stream):
    # Calculate the actual image size in the stream (accounting for rounding
    # of the resolution)
    fwidth = (width + 31) // 32 * 32
    fheight = (height + 15) // 16 * 16

    # Load the Y (luminance) data from the stream
    Y = np.frombuffer(stream, dtype=np.uint8, count=fwidth*fheight).\
            reshape((fheight, fwidth))
    # Load the UV (chrominance) data from the stream, and double its size
    U = np.frombuffer(stream, dtype=np.uint8, count=(fwidth//2)*(fheight//2)).\
            reshape((fheight//2, fwidth//2)).\
            repeat(2, axis=0).repeat(2, axis=1)
    V = np.frombuffer(stream, dtype=np.uint8, count=(fwidth//2)*(fheight//2)).\
            reshape((fheight//2, fwidth//2)).\
            repeat(2, axis=0).repeat(2, axis=1)
    # Stack the YUV channels together, crop the actual resolution, convert to
    # floating point for later calculations, and apply the standard biases
    YUV = np.dstack((Y, U, V))[:height, :width, :].astype(np.float)
    YUV[:, :, 0]  = YUV[:, :, 0]  - 16   # Offset Y by 16
    YUV[:, :, 1:] = YUV[:, :, 1:] - 128  # Offset UV by 128
    # YUV conversion matrix from ITU-R BT.601 version (SDTV)
    #              Y       U       V
    M = np.array([[1.164,  0.000,  1.596],    # R
                [1.164, -0.392, -0.813],    # G
                [1.164,  2.017,  0.000]])   # B
    # Take the dot product with the matrix to produce RGB output, clamp the
    # results to byte range and convert to bytes
    RGB = YUV.dot(M.T).clip(0, 255).astype(np.uint8)
    return RGB

try:
    frame = 1
    fps = 0
    index = 0
    start_time = time()
    while True:
        topic, payload = msg_receiver.recv()
        latency = time() - payload["timestamp"]
        image = convertYUVtoRGB2(payload['__raw_data__'][0])
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
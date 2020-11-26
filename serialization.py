import cv2
import numpy as np


def encode(frame, jpeg_quality=100):
    # JPEG quality, 0 - 100
    if jpeg_quality is None:
        jpeg_quality = 100
    ret_code, jpg_buffer = cv2.imencode(
        ".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality]
    )
    return ret_code, jpg_buffer


def decode(frame):
    return cv2.imdecode(np.frombuffer(frame, dtype="uint8"), -1)

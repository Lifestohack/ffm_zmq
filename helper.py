import numpy as np
import cv2


def YUVtoBGR(byteArray, width, height):
    px = width * height
    Y = np.frombuffer(byteArray[:px], np.uint8).reshape([height, width])
    u_end = px + (width // 2 * height // 2)
    U = byteArray[px:u_end]
    U = (
        np.frombuffer(U, dtype=np.uint8)
        .reshape((height // 2, width // 2))
        .repeat(2, axis=0)
        .repeat(2, axis=1)
    )
    V = byteArray[u_end:]
    V = (
        np.frombuffer(V, dtype=np.uint8)
        .reshape((height // 2, width // 2))
        .repeat(2, axis=0)
        .repeat(2, axis=1)
    )
    bgr = (np.dstack([Y, U, V])).astype(np.uint8)
    bgr = cv2.cvtColor(bgr, cv2.COLOR_YUV2BGR, 3)
    return bgr

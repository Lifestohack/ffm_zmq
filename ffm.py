import ffmpeg
import subprocess
import numpy as np
import sys
from scipy import ndimage
import helper


class VideoCapture:
    """
    Class for video capturing from video files, image sequences or cameras.
    """

    def __init__(self, source, pix_fmt="yuv420p"):
        self.source = source
        self.pix_fmt = pix_fmt
        self.width, self.height = self.get_video_size()  # or add custom values
        # Note: RGB24 == 3 bytes per pixel.
        self.setframeSize()

    def setResolution(self, width, height):
        self.width = width
        self.height = height
        self.setframeSize()

    def setframeSize(self):
        if self.pix_fmt == "bgr24":
            self.frame_size = self.width * self.height * 3
        elif self.pix_fmt == "yuv420p":
            self.frame_size = int(self.width * self.height * 1.5)
        else:
            raise NotImplementedError()

    def start(self):
        self.process = self.start_ffmpeg_process()

    def get_video_size(self):
        probe = ffmpeg.probe(self.source)
        video_info = next(s for s in probe["streams"] if s["codec_type"] == "video")
        width = int(video_info["width"])
        height = int(video_info["height"])
        return width, height

    def start_ffmpeg_process(self):
        args = (
            ffmpeg.input(self.source, framerate=32)
            .output(
                "pipe:",
                loglevel="quiet",
                format="rawvideo",
                s=f"{self.width}x{self.height}",
                pix_fmt=self.pix_fmt,
            )
            .compile()
        )
        return subprocess.Popen(args, stdout=subprocess.PIPE)

    def read(self):
        """
        Grabs, decodes and returns the next video frame.
        """
        in_bytes = self.grab()
        frame = self.retrieve(in_bytes)
        return frame

    def grab(self):
        """
        Grabs the next frame from video file or capturing device.
        """
        in_bytes = self.process.stdout.read(self.frame_size)
        # if sys.getsizeof(in_bytes) == 17:
        #     raise Exception("Read 0 byte. No image was grabed.")
        return in_bytes

    def retrieve(self, in_bytes):
        """
        Decodes and returns the grabbed video frame.
        """
        if len(in_bytes) == 0:
            frame = None
        else:
            assert len(in_bytes) == self.frame_size
        if self.pix_fmt == "bgr24":
            frame = np.frombuffer(in_bytes, np.uint8).reshape(
                [self.height, self.width, 3]
            )
        elif self.pix_fmt == "yuv420p":
            frame = helper.YUVtoBGR(in_bytes, self.width, self.height)
        else:
            raise NotImplementedError()

        return frame

    def release(self):
        self.process.kill()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.release()

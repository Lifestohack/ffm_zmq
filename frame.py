import ffmpeg
import cv2
import numpy as np
import subprocess
import logging as logger

class Ffmpegdata:
    def __init__(self, source):
        self.source = source
        self.width, self.height = self.get_video_size(source) # or add custom values


    def get_video_size(self, source):
        logger.info('Getting video size for {!r}'.format(source))
        probe = ffmpeg.probe(source)
        video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
        width = int(video_info['width'])
        height = int(video_info['height'])
        return width, height

    def start_ffmpeg_process(self):
        logger.info('Starting ffmpeg process')
        args = (
            ffmpeg
            .input(self.source)
            .output('pipe:', 
                    format='rawvideo', 
                    s=f'{self.width}x{self.height}', 
                    pix_fmt='rgb24')
            .compile()
        )
        return subprocess.Popen(args, stdout=subprocess.PIPE)

    def read_frame(self, process1, width, height):
        logger.debug('Reading frame')
        # Note: RGB24 == 3 bytes per pixel.
        frame_size = width * height * 3
        in_bytes = process1.stdout.read(frame_size)
        if len(in_bytes) == 0:
            frame = None
        else:
            assert len(in_bytes) == frame_size
            frame = (
                np
                .frombuffer(in_bytes, np.uint8)
                .reshape([height, width, 3])
            )
        return frame

    def start(self):
        self.process = self.start_ffmpeg_process()

    def read(self):
        return self.read_frame(self.process, self.width, self.height)
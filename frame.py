import os
import socket
import subprocess
import time
import sys
import numpy

class Ffmpegdata:
    command = 'ffmpeg ' \
              '-y ' \
              '-s 640x480 ' \
              '-pix_fmt rgb24 ' \
              '-i /dev/video0 ' \
              '-f rawvideo ' \
              '-an ' \
              '-'

    def __init__(self):
        self.p = subprocess.Popen(self.command.split(), 
        stdin=open(os.devnull), 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE)
        

    def get(self):
        data = self.p.stdout.read(640*480*3)
        if len(data) == 0:
            err = self.p.stderr.readlines()
            if len(err) > 0:
                print('Error')
                print(''.join([l.decode() for l in err]))
        return data
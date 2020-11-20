# ffmpeg

ffmpeg server:
Step 1: reads the bytes for the frame using ffmpeg.
step 2: creates a zmq server. 
step 3: sends the bytes with zmq server


ffmpeg server setting:

```sh

command = 'ffmpeg ' \
          '-y ' \
          '-s 640x480 ' \
          '-pix_fmt rgb24 ' \
          '-i /dev/video0 ' \
          '-f rawvideo ' \
          '-an ' \
          '-'

```

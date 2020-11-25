# ffmpeg

ffmpeg server:
1. Binds a zmq server. 
1. Reads the bytes for the using ffmpeg as yuv other pix_fmt as stated in ffmpeg.
3. Sends the bytes with tcp created by zmq server.

ffmpeg client:
1. Connects to the tcp server.
2. Reads the bytes and converts it to BGR if YUV format. Or Implement any custom format.
3. Shows it on the cv2 window.
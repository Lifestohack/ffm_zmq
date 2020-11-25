# Ffmpeg Server and client setup with Real time ZMQ server Implementation

ffmpeg server:
1. Binds a zmq server. 
1. Reads the bytes for the using ffmpeg as yuv other pix_fmt as stated in ffmpeg.
3. Sends the bytes with tcp created by zmq server.

ffmpeg client:
1. Connects to the tcp server.
2. Reads the bytes and converts it to BGR if YUV format. Or Implement any custom format.
3. Shows it on the cv2 window.

Usages:

# Make sure both client and server are on the same network

Step 1: change the server ip in ffm_server.py.
Step 2: Run it on the server.
Step 3: Change the ip address on ffm_client.py (same as the ip address of server)
step 4: Run the ffm_client.py on client.
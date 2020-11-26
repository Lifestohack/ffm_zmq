# Ffmpeg Server and client setup with Real time ZMQ server Implementation

This program helps you to stream real time video from one computer to another computer using ffmpeg.

Install Dependencies:
```sh
sudo apt install -y python3-opencv
sudo apt install -y ffmpeg

python3 -m install ffmpeg-python
python3 -m pip install pyzmq
python3 -m pip install msgpack==0.5.6
```
## How does it work?
Server:
1. Binds a zmq server. 
1. Reads the bytes for the using ffmpeg as yuv other pix_fmt as stated in ffmpeg.
3. Sends the bytes with tcp created by zmq server.

Client:
1. Connects to the tcp server.
2. Reads the bytes and converts it to BGR if YUV format. Or Implement any custom format.
3. Shows it on the cv2 window.

## Usages:

Note: Make sure both client and server are on the same network

1. Change the server ip in ffm_server.py.
2. Run it on the server.
3. Change the ip address on ffm_client.py (same as the ip address of server)
4. Run the ffm_client.py on client.

# ffmpeg

ffmpeg server:
1. reads the bytes for the using ffmpeg
2. creates a zmq server. 
3. sends the bytes with zmq server

ffmpeg client:
1. Connects to the tcp server
2. Reads the bytes and reshapes it to the original height and width
3. shows it on the cv2 window
from flask import Flask, render_template
from flask_socketio import SocketIO
import base64
import io
import os
from PIL import Image


app = Flask(__name__)
socketio = SocketIO(app)

if not os.path.exists('captured_images'):
    os.makedirs('captured_images')

global frame_counter
frame_counter = 0  # Initialize frame counter

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('video_data')
def handle_video_data(data):
    global frame_counter  # Declare frame_counter as global
    print("Received video data from client")

    # Decode base64 video data
    video_data = base64.b64decode(data.split(',')[1])

    # Open the video frame as an image using Pillow (PIL)
    image = Image.open(io.BytesIO(video_data))

    # Save the image to a folder
    image_path = os.path.join('captured_images', f'frame_{frame_counter}.jpg')
    image.save(image_path)

    print(f"Image saved: {image_path}")

    frame_counter += 1  # Increment frame counter


if __name__ == "__main__":
    socketio.run(app, debug=True)

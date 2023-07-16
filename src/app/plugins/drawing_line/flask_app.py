import cv2
import numpy as np
import os

from flask import Flask, request, jsonify


app = Flask(__name__)


def generate_drawing_line_video(coefficient):
    width, height = 512, 512
    num_frames = 100
    thickness = 8
    filename = 'drawing_line_video.mp4'

    # Generate random start and end points
    start_point = np.random.randint(0, width, size=(2,))
    end_point = np.random.randint(0, width, size=(2,))
    color = (0, 0, 0)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, fourcc, 30.0, (width, height))

    current_point = start_point

    frame = np.ones((height, width, 3), dtype=np.uint8) * 255

    for i in range(num_frames):
        t = i / num_frames
        prev_point = current_point
        current_point = (int((1 - t) * start_point[0] + t * end_point[0]), int((1 - t) * start_point[1] + t * end_point[1]))

        cv2.line(frame, prev_point, current_point, color, thickness)

        # Fade out old parts of the line
        frame = 255 - ((255 - frame) * coefficient).astype("uint8")

        out.write(frame)

    out.release()

    return filename


@app.route('/', methods=['POST'])
def predict():
    args = request.json
    coefficient = float(args['message'].split()[1])
    video_path = generate_drawing_line_video(coefficient)
    return jsonify({
        'file': os.path.abspath(video_path)
    })


if __name__ == '__main__':
    app.run('0.0.0.0', port=10037)

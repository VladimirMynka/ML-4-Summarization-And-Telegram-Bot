import os
import random
from PIL import Image
import numpy as np

from flask import Flask, request, jsonify

app = Flask(__name__)

def generate_coloured_image(color):
    palette = {
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'yellow': (255, 255, 0),
        'orange': (255, 165, 0),
        'purple': (128, 0, 128),
        'pink': (255, 192, 203),
        'gray': (128, 128, 128),
        'brown': (139, 69, 19),
        'black': (0, 0, 0),
        'white': (255, 255, 255)
    }
   
    width, height = 512, 512
    image = np.zeros((height, width, 3), dtype=np.uint8)
    predominant_color = palette[color.lower()]
    for i in range(height):
        for j in range(width):
            image[i][j] = [(random.randint(0, 255) + predominant_color[k]) // 2 for k in range(3)]
    
    image_path = os.path.join(os.getcwd(), 'coloured_image.png')
    img = Image.fromarray(image)
    img.save(image_path)
    
    return image_path

@app.route('/', methods=['POST'])
def predict():
    args = request.json
    color = args.get('message')

    if color is None:
        return jsonify({'text': 'No color provided.'})

    image_path = generate_coloured_image(color)

    return jsonify({'image': image_path})

if __name__ == '__main__':
    app.run('0.0.0.0', port=10035)

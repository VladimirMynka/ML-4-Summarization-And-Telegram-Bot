import numpy as np
import random
import string
import os

from flask import Flask, request, jsonify
from pydub import AudioSegment

app = Flask(__name__)

def generate_music():
    notes = []
    for _ in range(100):
        note = random.choice(string.ascii_uppercase[:7])
        notes.append(note)
    frequencies = {
        'A': 440,
        'B': 494,
        'C': 523,
        'D': 587,
        'E': 659,
        'F': 698,
        'G': 784
    }
    music = []
    duration = 15000  # in milliseconds
    for note in notes:
        frequency = frequencies[note]
        t = np.arange(duration)
        signal = np.sin(2 * np.pi * frequency * t / 44100)
        music.extend(signal)
    audio_data = np.array(music, dtype=np.float32)
    audio_data /= np.max(np.abs(audio_data))
    audio_data = (audio_data * 32767).astype(np.int16)
    file_path = 'generated_music.mp3'
    audio_segment = AudioSegment(audio_data.tobytes(), frame_rate=44100, sample_width=2, channels=1)
    audio_segment.export(file_path, format='mp3')
    return os.path.abspath(file_path)

@app.route('/', methods=['POST'])
def predict():
    args = request.json
    message = args['message']
    gpt = args['gpt_response']

    if 'music' in gpt:
      return jsonify({
          'audio': generate_music()
      })

    return jsonify({
        'text': 'The plugin was not activated'
    })

if __name__ == '__main__':
    app.run('0.0.0.0', port=10032)

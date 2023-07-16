import subprocess

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def predict():
    args = request.json
    message = args['message']
    gpt = args['gpt_response']

    command = message.strip()
    output = ''

    if command.startswith('ls') or command.startswith('cat'):
        try:
            output = subprocess.check_output(["powershell"] + command.split(), universal_newlines=True)
        except Exception as e:
            output = str(e)
    
    return jsonify({
        'text': output.strip()
    })


if __name__ == '__main__':
    app.run('0.0.0.0', port=10023)

import logging

from flask import Flask, request, jsonify

app = Flask(__name__)

board = [[' ' for _ in range(3)] for _ in range(3)]
current_player = 'X'

def make_move(player, row, col):
    if board[row][col] == ' ':
        board[row][col] = player
        return True
    return False


def reset_board():
    global board, current_player
    board = [[' ' for _ in range(3)] for _ in range(3)]
    current_player = 'X'


@app.route('/', methods=['POST'])
def play_tic_tac_toe():
    global current_player
    args = request.json
    message = args['message']
    gpt = args['gpt_response']
    response = {}

    move = message.strip().split()

    if move[0] == 'clear':
        reset_board()
        response['text'] = get_board_string()
        return jsonify(response)

    if len(move) < 3:
        response['text'] = 'Invalid move format'
        return jsonify(response)

    else:
        try:
            row = int(move[1])
            col = int(move[2])
            if make_move(current_player, row, col):
                current_player = 'O' if current_player == 'X' else 'X'
            response['text'] = get_board_string()
        except (ValueError, IndexError):
            response['text'] = 'Invalid move'

    return jsonify(response)


def get_board_string():
    board_string = ''
    for row in board:
        board_string += '|'.join(row) + '\n'
        board_string += '-----\n'
    return board_string


if __name__ == '__main__':
    app.run('0.0.0.0', port=10034)

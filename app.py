from flask import Flask, request, jsonify, render_template, url_for
from models.Board import DominoBoard
from config import Config
import utils.SvgGens as SvgGens
import utils.helpers as Helpers
import utils.Solver as Solver

app = Flask(__name__)
app.config.from_object(Config)

board = DominoBoard()

@app.route('/')
def home():
    board.rows = Config.START_ROWS
    board.cols = Config.START_COLS
    board.filepath = Config.FILE_PATH
    board.filename = ''
    return render_template(Config.HTML_TEMPLATE, css=Config.CSS_TEMPLATE, board=board)

@app.route('/reset')
def reset():
    print(board.to_dict())
    board.rows = Config.START_ROWS
    board.cols = Config.START_COLS
    board.filepath = Config.FILE_PATH
    board.filename = ''
    board.row_targets = []
    board.col_targets = []
    board.blocked = set()
    print(board.to_dict())
    return jsonify({ 'board': board.to_dict() })

@app.route('/grid-data', methods=['POST'])
def grid_data():
    try:
        data = request.get_json(force=True)
        #print(f'pre update:  {board.to_dict()}')

        board.blocked = set()

        # Validate 'type' is a string
        type = data.get('type')
        if not isinstance(type, str):
            return jsonify({ 'board': board.to_dict() }), 400

        # Validate 'value' is an integer
        value_raw = data.get('value')
        try:
            value = int(value_raw)
        except (ValueError, TypeError):
            return jsonify({ 'board': board.to_dict() }), 400

        # Proceed with valid data
        if (type == 'rows'):
            board.rows = value
        elif (type == 'cols'):
            board.cols = value

        if board.row_targets:
            Helpers.update_array(board.row_targets, 0, board.row_targets[0], value)
        if board.col_targets:
            Helpers.update_array(board.col_targets, 0, board.col_targets[0], value)

        #print(f'post update: {board.to_dict()}')
        return jsonify({ 'board': board.to_dict() })

    except Exception as e:
        return jsonify({ 'board': board.to_dict() }), 400

@app.route('/cell-click', methods=['POST'])
def cell_click():
    data = request.get_json()
    row = data['row']
    col = data['col']

    if ((row, col) in board.blocked):
        color = '#F0F0F0'
        board.blocked.remove((row, col))
    else:
        # Set cell to blocked
        color = '#757575'
        board.blocked.add((row, col))

    return jsonify({'message': 'Cell updated', 'color': color, 'board': board.to_dict()})

@app.route('/label-update', methods=['POST'])
def label_update():
    data = request.get_json()
    label_type = data['type']  # 'row' or 'col'
    index = data['index']
    value = data['value']

    if (label_type == 'row'):
        Helpers.update_array(board.row_targets, index, value)
    elif (label_type == 'col'):
        Helpers.update_array(board.col_targets, index, value)

    return jsonify({'board': board.to_dict()})

@app.route('/generate-click', methods=['POST'])
def generateSvg():
    result = Solver.solve_domino_puzzle(board)
    if result:
        board.filename = Config.FILE_NAME
        print(board.to_dict())
        f = f'{board.filepath}/{board.filename}'
        SvgGens.generate_svg_from_result(result, f)
    else:
        board.filename = None
    return jsonify({'board': board.to_dict()})

if __name__ == '__main__':
    app.run(debug=True)

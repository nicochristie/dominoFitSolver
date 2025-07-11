from models.Board import DominoBoard
from datetime import datetime
import utils.Solver as Solver
import utils.SvgGens as SvgGens

save_path = f'.\\Solved\\'
def solve(board, date, puzzle_number):
    result = Solver.solve_domino_puzzle(board)
    f = f'{save_path}{date.strftime('%d-%m-%Y')} {len(board.row_targets)}x{len(board.col_targets)} {puzzle_number}.svg'
    SvgGens.generate_svg_from_result(result, f)

board = DominoBoard()

# 01.07.2025 6x6 1
board.blocked = {(0,1), (1,3), (2,1), (2,3), (2,5), (3,3), (3,5), (5,3)}
board.row_targets = [5, 2, 3, 1, 5, 2]
board.col_targets = [3, 1, 5, 4, 3, 2]
#solve(board, datetime.today(), 1)

# 01.07.2025 7x7 2
board.blocked = {(0,0), (0,1), (0,4), (1,5), (2,5), (3,6), (6,4)}
board.row_targets = [4, 4, 2, 4, 7, 6, 2]
board.col_targets = [2, 6, 3, 5, 1, 6, 6]
#solve(board, datetime.today(), 2)

# 01.07.2025 7x7 3
board.blocked = {(0,5), (1,5), (2,0), (2,3),(3,5)}
board.row_targets = [6, 2, 5, 3, 6, 7, 4]
board.col_targets = [3, 3, 3, 8, 6, 2, 8]
#solve(board, datetime.today(), 3)

# Asymetric test 
board.blocked = {(2, 2), (3, 2)}
board.row_targets = [3, 2, 2, 2]
board.col_targets = [0, 8, 1]
solve(board, datetime.today(), 1)

from ortools.sat.python import cp_model

from models.Board import DominoBoard

def solve_domino_puzzle(board: DominoBoard):
    model = cp_model.CpModel()
    rows = len(board.row_targets)
    columns = len(board.col_targets)
    h_domino = {}
    v_domino = {}

    if (rows == 0 or columns == 0):
        return None

    # Define variables for horizontal and vertical dominoes
    for r in range(rows):
        for c in range(columns):
            if c < columns - 1 and (r, c) not in board.blocked and (r, c+1) not in board.blocked:
                h_domino[(r, c)] = model.NewBoolVar(f'h_{r}_{c}')
            if r < rows - 1 and (r, c) not in board.blocked and (r+1, c) not in board.blocked:
                v_domino[(r, c)] = model.NewBoolVar(f'v_{r}_{c}')

    # Ensure no overlapping dominoes
    for r in range(rows):
        for c in range(columns):
            if (r, c) not in board.blocked:
                coverage = []
                if (r, c) in h_domino:
                    coverage.append(h_domino[(r, c)])
                if (r, c-1) in h_domino:
                    coverage.append(h_domino.get((r, c-1), 0))
                if (r, c) in v_domino:
                    coverage.append(v_domino[(r, c)])
                if (r-1, c) in v_domino:
                    coverage.append(v_domino.get((r-1, c), 0))
                if coverage:
                    model.Add(sum(coverage) <= 1)

    # Row constraints
    for r in range(rows):
        row_sum = []
        for c in range(columns):
            if (r, c) in h_domino:
                row_sum.append(h_domino[(r, c)] * 2)
            if (r, c) in v_domino:
                row_sum.append(v_domino[(r, c)])
        model.Add(sum(row_sum) == board.row_targets[r])

    # Column constraints
    for c in range(columns):
        col_sum = []
        for r in range(rows):
            if (r, c-1) in h_domino:
                col_sum.append(h_domino.get((r, c-1), 0) * 2)
            if (r, c) in v_domino:
                col_sum.append(v_domino[(r, c)])
        model.Add(sum(col_sum) == board.col_targets[c])

    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Build result matrix
    blocked_cell = -1
    result = [[blocked_cell for _ in range(columns)] for _ in range(rows)]
    if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        for (r, c), var in h_domino.items():
            print(f'r: {r}, c: {c}, var: {var}')
            if solver.Value(var):
                result[r][c] = 0.1
                result[r][c+1] = 2
        for (r, c), var in v_domino.items():
            print(f'r: {r}, c: {c}, var: {var}')
            if solver.Value(var):
                result[r][c] = 1
                result[r+1][c] = -0.1

    return result

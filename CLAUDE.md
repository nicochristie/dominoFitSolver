# DominoFit Solver - Claude Code Context

## Project Overview

This is a **solver tool** for the DominoFit puzzle game (https://dominofit.isotropic.us/). It is NOT a recreation of the game itself, but rather a utility to solve puzzles programmatically.

### What This Tool Does
- Provides a web UI to input DominoFit puzzle constraints
- Uses Google OR-Tools constraint programming solver to find valid domino placements
- Generates SVG visualizations of solutions
- Validates puzzle configurations

### What This Tool Is NOT
- Not an interactive game where users place dominoes manually
- Not trying to replicate the DominoFit game experience
- Not a puzzle generator (yet - see ROADMAP)

## Project Structure

```
dominoFitSolver/
├── app.py                 # Flask web application (main entry point)
├── config.py              # Configuration settings
├── models/
│   └── Board.py          # DominoBoard data model
├── utils/
│   ├── Solver.py         # OR-Tools constraint solver (core logic)
│   ├── SvgGens.py        # SVG generation for solutions
│   ├── DominoFit.py      # Example puzzles and batch solving
│   └── helpers.py        # Array manipulation utilities
├── templates/            # Jinja2 HTML templates
│   ├── index.html.j2     # Main UI template
│   ├── base.html.j2      # Base template
│   └── builder.html      # Board builder page
├── static/
│   ├── css/style.css     # Styling
│   └── dominoFit.svg     # Generated solution output
└── docs/
    ├── DominoFit Example.png  # Reference game screenshot
    └── ROADMAP.md        # Future development plans

```

## How It Works

### 1. Puzzle Input
Users specify:
- Grid size (rows × columns)
- Blocked cells (gray squares that can't have dominoes)
- Row constraints (sum of domino dots per row)
- Column constraints (sum of domino dots per column)

### 2. Constraint Solving
The solver (`utils/Solver.py`) uses Google OR-Tools CP-SAT solver to:
- Place dominoes (1×2 tiles) horizontally and vertically
- Ensure no overlapping dominoes
- Satisfy row/column dot sum constraints
- Each domino contributes: 1 dot (single side) + 2 dots (double side) = 3 dots total

### 3. Visualization
Solutions are rendered as SVG graphics showing:
- Placed dominoes with dots
- Blocked cells in gray
- Clear domino boundaries

## Key Files to Understand

### `app.py` (Flask Routes)
- `/` - Home page with board builder
- `/grid-data` - Update board dimensions
- `/cell-click` - Toggle cells as blocked
- `/label-update` - Set row/column constraints
- `/generate-click` - Solve puzzle and generate SVG
- `/reset` - Reset board to defaults

### `utils/Solver.py` (Core Algorithm)
Uses constraint programming to model the problem:
- Variables: `h_domino[(r,c)]` and `v_domino[(r,c)]` for horizontal/vertical dominoes
- Constraints:
  - Each non-blocked cell covered by exactly 0 or 1 domino (no overlaps)
  - Row sums match targets
  - Column sums match targets
- Solver finds feasible solution or returns None

### `models/Board.py` (Data Model)
```python
class DominoBoard:
    rows: int
    cols: int
    blocked: set[tuple]      # Set of (row, col) blocked cells
    row_targets: list[int]   # Target dot sums for each row
    col_targets: list[int]   # Target dot sums for each column
```

## Development Setup

### Prerequisites
- Python 3.8+
- pip

### Installation
```bash
# Install dependencies
pip install -e .

# Run the app
python app.py

# Access at http://localhost:5000
```

### Dependencies
- `flask` - Web framework
- `ortools` - Constraint programming solver
- `svgwrite` - SVG generation

## Common Tasks

### Running the Web App
```bash
python app.py
```

### Testing Example Puzzles
Edit `utils/DominoFit.py` and uncomment test cases, then:
```bash
python utils/DominoFit.py
```

### Debugging
The project includes VS Code configuration:
- `launch.json` - Debug configuration
- `tasks.json` - Browser auto-open task

## Known Limitations

1. **Single-user only**: Uses global `board` object (app.py:11) - multiple concurrent users will conflict
2. **No puzzle validation**: Doesn't check if puzzle is solvable before running solver
3. **Basic UI**: Functional but doesn't match game aesthetic
4. **No undo/redo**: Can't track state changes
5. **No multiple solutions**: Only shows first solution found

## Future Plans

See `docs/ROADMAP.md` for detailed future development plans including:
- Screenshot-to-puzzle using local LLM (Ollama)
- Multi-project architecture with separate backend API
- UI improvements to match game look
- Multiple solution enumeration
- Puzzle difficulty analysis

## Tips for Claude Code

### When Adding Features
- The solver logic is working correctly - don't fix what isn't broken
- Focus on UX improvements and new features rather than core algorithm changes
- Consider multi-user sessions when adding backend features

### Project Style
- Uses Flask for web framework (not FastAPI or Django)
- Simple, functional code style - no over-engineering
- Jinja2 templates for HTML rendering
- SVG for graphics (not Canvas or other formats)

### Testing Strategy
- Use `utils/DominoFit.py` for batch testing puzzles
- Example puzzles include real puzzles from the game
- Visual verification of SVG output is primary testing method

## Contact
Nicolas Christie - nicolas.christie@gmail.com

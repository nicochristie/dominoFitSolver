# dominoFitSolver

Domino Fit Solver is a web application for solving and visualizing domino tiling puzzles. It provides a user-friendly interface to input board sizes and constraints, and uses optimization algorithms to find valid domino placements.

## Features
- Web interface built with Flask
- Customizable board size and constraints
- Visualization of domino solutions as SVG graphics
- Uses Google OR-Tools for efficient solving
- Downloadable SVG output

## Project Structure
- `app.py`: Main Flask application
- `models/`: Board and puzzle models
- `utils/`: Solver logic, SVG generation, and helpers
- `static/`: CSS and static assets
- `templates/`: Jinja2 HTML templates
- `config.py`: Configuration settings

## Requirements
- Python 3.8+
- Flask
- ortools
- svgwrite

## Installation
1. Clone the repository:
   ```sh
   git clone <repo-url>
   cd "DF Solver"
   ```
2. Install dependencies:
   ```sh
   pip install .
   ```

## Usage
Run the web application:
```sh
python app.py
```
Then open your browser at `http://localhost:5000`.

## License
MIT License

## Author
Nicolas Christie

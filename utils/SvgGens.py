from collections import namedtuple
import svgwrite

Line = namedtuple('Line', ['start', 'end'])

def generate_svg_from_result(result, filename='domino_solution.svg', board_size=350):
    rows = len(result)
    columns = len(result[0]) if result else 0
    cell_size = board_size / rows

    dwg = svgwrite.Drawing(filename, size=(cell_size * columns, cell_size * rows))

    for r in range(rows):
        for c in range(columns):
            x = c * cell_size
            y = r * cell_size
            draw_dots_cell(dwg, cell_size, x, y, result[r][c])

    dwg.save()

def draw_line(dwg, line: Line, color='black'):
    dwg.add(dwg.line(start=line.start, end=line.end, stroke=color, stroke_width=1))

def draw_dots_cell(dwg, cell_size, x, y, dots):
    dot_radius = cell_size / 8
    offset = dot_radius * 1.5
    center = (x + cell_size / 2, y + cell_size / 2)
    dim_line_color = '#DDDDDD'

    # Draw cell background
    dwg.add(dwg.rect(insert=(x, y), size=(cell_size, cell_size), fill='white', stroke='none'))

    # Define sides using Line namedtuples
    sides = {
        'top': Line((x, y), (x + cell_size, y)),
        'right': Line((x + cell_size, y), (x + cell_size, y + cell_size)),
        'bottom': Line((x + cell_size, y + cell_size), (x, y + cell_size)),
        'left': Line((x, y + cell_size), (x, y)),
    }

    if dots == -1:
        dwg.add(dwg.rect(insert=(x+1, y+1), size=(cell_size-2, cell_size-2), fill='gray', stroke='black'))
    if dots == 0.1: # 0 dots box for the 2 dots domino
        for side in ['top', 'left', 'bottom']:
            draw_line(dwg, sides[side])
    elif dots == -0.1: # 0 dots box for the 1 dot domino
        for side in ['left', 'right', 'bottom']:
            draw_line(dwg, sides[side])
    elif dots == 1: # 1 dot box for the 1 dot domino
        dwg.add(dwg.circle(center=center, r=dot_radius, fill='black'))
        for side in ['top', 'left', 'right']:
            draw_line(dwg, sides[side])
        draw_line(dwg, sides['bottom'], color=dim_line_color)
    elif dots == 2: # 2 dots box for the 2 dots domino
        dwg.add(dwg.circle(center=(center[0] - offset, center[1] - offset), r=dot_radius, fill='black'))
        dwg.add(dwg.circle(center=(center[0] + offset, center[1] + offset), r=dot_radius, fill='black'))
        for side in ['top', 'right', 'bottom']:
            draw_line(dwg, sides[side])
        draw_line(dwg, sides['left'], color=dim_line_color)

import svg
from lithomancy import Stick


def output(sticks: list[Stick]) -> svg.SVG:
    """
    Generates an SVG representation of the sticks source code.
    The "beach" on which the sticks are laid out.
    """
    COLORS = {'a': 'magenta', 'b': 'blue', 'c': 'yellow', 'g': 'grey'}
    WIDTH = 500
    HEIGHT = 500
    ppu=10
    beach = svg.SVG(width=WIDTH, height=HEIGHT)
    defs = svg.Defs(
        elements=[
            svg.Marker(
                id='arrow',
                orient='auto-start-reverse',
                refX=2,
                refY=2,
                markerWidth=3,
                markerHeight=3,
                elements=[
                    svg.Path(
                        d='M 0 0 L 4 2 L 0 4 z',
                        fill_opacity=0.3, 
                        )]) ])
    elements = [defs, svg.Circle(cx=WIDTH//2, cy=HEIGHT//2, r=1, stroke='red')]

    for s in sticks:
        elements.append(
           svg.Line(
                x1=ppu * s.a[0] + WIDTH // 2, x2=ppu * s.b[0] + WIDTH // 2,
                y1=ppu * s.a[1] + HEIGHT // 2, y2=ppu * s.b[1] + HEIGHT // 2,
                stroke=COLORS[s.material],
                stroke_width=1,
                marker_end='url(#arrow)',
            )
        )
    beach.elements = elements
    return beach

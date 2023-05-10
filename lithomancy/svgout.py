import svg
from lithomancy import Stick


def arrow():
    return svg.Marker(
        id='arrow',
        orient='auto-start-reverse',
        refX=2,
        refY=2,
        markerWidth=3,
        markerHeight=3,
        elements=[
            svg.Path(
                d='M 0 0 L 4 2 L 0 4 z',
                fill_opacity=0.3
         )])


def dot():
    return svg.Marker(
        id='dot',
        orient='auto-start-reverse',
        refX=2,
        refY=2,
        markerWidth=3,
        markerHeight=3,
        elements=[
            svg.Circle(
                cx=2, cy=2, r=1,
                fill_opacity=0.3
         )])


def bounds(sticks: list[Stick]) -> tuple:
    WIDTH = 500
    HEIGHT = 500

    # returns width, height, offset
    return WIDTH, HEIGHT, (WIDTH // 2, HEIGHT // 2)


def output(sticks: list[Stick], arrows: bool = False) -> svg.SVG:
    """
    Generates an SVG representation of the sticks source code.
    The "beach" on which the sticks are laid out.
    """
    COLORS = {'a': 'magenta', 'b': 'blue', 'c': 'yellow', 'g': 'grey'}
    ppu = 10
    w, h, offset = bounds(sticks)
    beach = svg.SVG(width=w, height=h)
    elements = []
    marker = arrow() if arrows else dot()
    defs = svg.Defs(
        elements=[marker]
    )
    elements = [defs, svg.Circle(cx=offset[0], cy=offset[1], r=1, stroke='red')]

    for s in sticks:
        elements.append(
           svg.Line(
                x1=ppu * s.a[0] + offset[0], x2=ppu * s.b[0] + offset[0],
                y1=ppu * s.a[1] + offset[1], y2=ppu * s.b[1] + offset[1],
                stroke=COLORS[s.material],
                stroke_width=1,
                marker_end=f'url(#{marker.id})',
            )
        )
    beach.elements = elements
    return beach

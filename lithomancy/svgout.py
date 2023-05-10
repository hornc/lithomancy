import svg
from lithomancy import Stick


PPU = 10  # pixels per unit


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


def bounds(sticks: list[Stick], margin: int = 2 * PPU) -> tuple:
    x_max = x_min = sticks[0].a[0]
    y_max = y_min = sticks[0].a[1]

    for s in sticks:
        x_max = max(x_max, s.a[0], s.b[0])
        x_min = min(x_min, s.a[0], s.b[0])
        y_max = max(y_max, s.a[1], s.b[1])
        y_min = min(y_min, s.a[1], s.b[1])
    width = PPU * (x_max - x_min) + 2 * margin
    height = PPU * (y_max - y_min) + 2 * margin

    # returns width, height, offset
    return width, height, (-x_min * PPU + margin , y_min * PPU + margin)


def output(sticks: list[Stick], arrows: bool = False) -> svg.SVG:
    """
    Generates an SVG representation of the sticks source code.
    The "beach" on which the sticks are laid out.
    """
    COLORS = {'a': 'magenta', 'b': 'blue', 'c': 'yellow', 'g': 'grey'}

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
                x1=PPU * s.a[0] + offset[0], x2=PPU * s.b[0] + offset[0],
                y1=PPU * s.a[1] + offset[1], y2=PPU * s.b[1] + offset[1],
                stroke=COLORS[s.material],
                stroke_width=1,
                marker_end=f'url(#{marker.id})',
            )
        )
    beach.elements = elements
    return beach

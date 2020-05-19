from charts.colors import color_arr
from charts.scale import scale
from reportlab.graphics.shapes import Line, String, rotate, Circle, Rect, PolyLine


def add_chart_to_page(page, chart):
    for item in chart:
        page.add(item)
    return page


def circle(x, y, r, fill_color="#000000", border_color="#000000", border_width=1):
    return Circle(x, y, r, fillColor=fill_color, strokeColor=border_color, strokeWidth=border_width)


def path(points, color):
    return PolyLine(points, strokeColor=color, strokeWidth=0.5)


def rect(x, y, width, height, border_color, fill_color, opacity):
    return Rect(x,
                y,
                width,
                height,
                strokeColor=border_color,
                fillColor=fill_color,
                strokeOpacity=opacity,
                fillOpacity=opacity,
                strokeWidth=0.5
                )


def x_axis_lines(x_axis, y_axis):
    lines = []
    for tic in x_axis["tics"]:
        x = scale(tic, x_axis)
        lines.append(
            Line(
                x,
                scale(y_axis["min"], y_axis),
                x,
                scale(y_axis["max"], y_axis),
                strokeDashArray=[2, 2],
                strokeOpacity=0.4,
                strokeWidth=0.5
            )
        )

    return lines


def x_axis_tics(x_axis, y_axis):
    tics = [
        Line(
            scale(x_axis["min"], x_axis),
            scale(y_axis["min"], y_axis),
            scale(x_axis["min"], x_axis),
            scale(y_axis["max"], y_axis),
            strokeWidth=0.5
        )
    ]

    for tic in x_axis["tics"]:
        tics.append(
            Line(
                scale(tic, x_axis),
                scale(y_axis["min"], y_axis),
                scale(tic, x_axis),
                scale(y_axis["min"], y_axis) - 4,
                strokeWidth=0.5
            )
        )

    return tics


def y_axis_lines(x_axis, y_axis):
    lines = []
    for tic in y_axis["tics"]:
        y = scale(tic, y_axis)
        lines.append(
            Line(
                scale(x_axis["min"], x_axis),
                y,
                scale(x_axis["max"], x_axis),
                y,
                strokeOpacity=0.4,
                strokeDashArray=[2, 2],
                strokeWidth=0.5
            )
        )

    return lines


def y_axis_tics(x_axis, y_axis, side):
    if side == "left":
        x1 = scale(x_axis["min"], x_axis) - 4
        x2 = scale(x_axis["min"], x_axis)
    else:
        x1 = scale(x_axis["max"], x_axis)
        x2 = scale(x_axis["max"], x_axis) + 2

    tics = [
        Line(
            scale(x_axis["min"], x_axis),
            scale(y_axis["min"], y_axis),
            scale(x_axis["max"], x_axis),
            scale(y_axis["min"], y_axis),
            strokeWidth=0.5
        )
    ]

    for tic in y_axis["tics"]:
        tics.append(
            Line(
                x1,
                scale(tic, y_axis),
                x2,
                scale(tic, y_axis),
                strokeWidth=0.5
            )
        )

    return tics


def x_axis_text(x_axis, y_axis):
    txt = []
    for tic in x_axis["tics"]:
        txt.append(
            String(
                scale(tic, x_axis) - 2,
                scale(y_axis["min"], y_axis) - 10,
                "%s" % tic,
                fontSize=8,
                fontName="Helvetica"
            )
        )

    return txt


def x_axis_title(x_axis, y_axis):
    x = ((x_axis["max"] - x_axis["min"]) / 2) + x_axis["min"]
    return [
        String(
            scale(x, x_axis) - (len(x_axis["title"]) * 6),
            scale(y_axis["min"], y_axis) - 22,
            x_axis["title"],
            fontSize=11,
            fontName="Helvetica"
        )
    ]


def y_axis_text(x_axis, y_axis, side):
    if side == "left":
        x = scale(x_axis["min"], x_axis) - 5
        anchor = "end"
    else:
        x = scale(x_axis["max"], x_axis) + 5
        anchor = "start"

    txt = []
    for tic in y_axis["tics"]:
        txt.append(
            String(
                x,
                scale(tic, y_axis) - 2,
                "%s" % tic,
                fontSize=8,
                fontName="Helvetica",
                textAnchor=anchor
            )
        )

    return txt


def y_axis_title(x_axis, y_axis, side):
    if side == "left":
        x = scale(y_axis["min"], y_axis)
        y = -(scale(x_axis["min"], x_axis)) + 20
        tf = rotate(90)
    else:
        x = -(scale(y_axis["max"], y_axis))
        y = scale(x_axis["max"], x_axis) + 20
        tf = rotate(270)
    return [
        String(
            x,
            y,
            y_axis["title"],
            transform=tf,
            fontSize=11,
            fontName="Helvetica"
        )
    ]


def title(txt, x_axis, y_axis):
    return [
        String(
            scale(x_axis["min"], x_axis),
            scale(y_axis["max"], y_axis) + 3,
            txt,
            fontSize=12,
            fontName="Helvetica"
        )
    ]


def get_keys(key_items, x_axis, y_axis, element_type="line"):
    keys = []
    x = scale(x_axis["max"], x_axis) + 30
    y = scale(y_axis["max"], y_axis)
    for idx, key in enumerate(key_items):
        color = color_arr[idx % len(color_arr)]
        y_val = y - (15 * (idx + 1))
        keys.append(get_key_symbol(x, y_val, element_type, color))
        keys.append(String(x + 14, y_val, key.split('_')[0], fontName="Helvetica", fontSize=8))

    return keys


def get_key_symbol(x, y, element_type, color):
    return {
        "line": Line(x, y + 3, x + 10, y + 3, strokeColor=color, strokeWidth=3),
        "circle": Circle(x + 6, y + 3, 2, fillColor=color, strokeColor=color),
        "rect": Rect(x + 6, y, 4, 4, fillColor=color, strokeColor=color),
    }[element_type]


def right_axis_line(x_axis, y_axis):
    return [
        Line(
            scale(x_axis["max"], x_axis),
            scale(y_axis["min"], y_axis),
            scale(x_axis["max"], x_axis),
            scale(y_axis["max"], y_axis),
            strokeWidth=0.5
        )
    ]


def add_star_to_13(x_axis, y_axis):
    return [
        String(
            scale(13, x_axis) - 7,
            scale(y_axis["min"], y_axis) - 14,
            "*",
            fontSize=14,
            fontName="Helvetica"
        )
    ]
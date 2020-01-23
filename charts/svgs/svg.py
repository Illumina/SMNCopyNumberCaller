import math

from charts.colors import color_arr
from charts.scale import scale, y_scale


class SvgElement:
    def __init__(self, name, attrs, value=None):
        self.name = name
        self.value = value
        self.attrs = attrs

    def to_string(self):
        result = "<%s" % self.name

        for attr in self.attrs:
            result += " %s=\"%s\"" % (attr[0], attr[1])
        result += ">"

        if self.value is not None:
            for v in self.value:
                if type(v) is str:
                    result += v
                else:
                    result += v.to_string()
        result += "</%s>" % self.name

        return result

    def add_attr(self, attr_tuple):
        self.attrs.append(attr_tuple)

    def modify_attr(self, attr_tuple):
        for attr in self.attrs:
            if attr[0] == attr_tuple[0]:
                attr[1] = attr_tuple[1]


def line(x1, y1, x2, y2, color="black", thickness=1, opacity=1.0, dashes=0):
    return SvgElement("line", [
        ("x1", x1),
        ("x2", x2),
        ("y1", y1),
        ("y2", y2),
        ("stroke", color),
        ("stroke-width", thickness),
        ("opacity", opacity),
        ("stroke-dasharray", dashes)
    ])


def rect(x, y, width, height, border_color="black", fill_color="black", border_width=1, corner_radius=0, opacity=1.0):
    return SvgElement("rect", [
        ("x", x),
        ("y", y),
        ("width", width),
        ("height", height),
        ("stroke", border_color),
        ("stroke-width", border_width),
        ("fill", fill_color),
        ("rx", corner_radius),
        ("opacity", opacity)
    ])


def circle(x, y, r, fill_color="black", border_color="black", border_width="black"):
    return SvgElement("circle", [
        ("cx", x),
        ("cy", y),
        ("r", r),
        ("stroke", border_color),
        ("stroke-width", border_width),
        ("fill", fill_color)
    ])


def text(x, y, txt, style="font: 13px sans-serif", transform=""):
    return SvgElement("text", [
        ("x", x),
        ("y", y),
        ("style", style),
        ("transform", transform)
    ], txt)


def path(points, color="black", thickness=1, dashes=0, opacity=1.0):
    return SvgElement("polyline", [
        ("points", " ".join(points)),
        ("stroke", color),
        ("fill", "none"),
        ("stroke-width", thickness),
        ("opacity", opacity),
        ("stroke-dasharray", dashes)
    ])


def add_tooltip(element, txt):
    title_el = SvgElement("title", [], txt)
    if element.value is None:
        element.value = [title_el]
    else:
        element.value += title_el

    return element


def headers(height=None):
    svg = SvgElement("svg", [
        ("xmlns", "http://www.w3.org/2000/svg"),
        ("xmlns:xlink", "http://www.w3.org/1999/xlink")
    ])
    if height is not None:
        svg.add_attr(("style", "height: %s" % height))
    return svg


def x_axis_lines(x_axis, y_axis):
    lines = []
    for tic in x_axis["tics"]:
        x = scale(tic, x_axis)
        lines.append(
            line(
                x,
                y_scale(y_axis["min"], y_axis),
                x,
                y_scale(y_axis["max"], y_axis),
                opacity=0.5,
                dashes=3
            )
        )

    return lines


def x_axis_tics(x_axis, y_axis):
    tics = [
        line(
            scale(x_axis["tics"][0], x_axis),
            y_scale(y_axis["min"], y_axis),
            scale(x_axis["tics"][0], x_axis),
            y_scale(y_axis["max"], y_axis)
        )
    ]

    for tic in x_axis["tics"]:
        tics.append(
            line(
                scale(tic, x_axis),
                y_scale(y_axis["min"], y_axis),
                scale(tic, x_axis),
                y_scale(y_axis["min"], y_axis) + 6
            )
        )

    return tics


def x_axis_text(x_axis, y_axis):
    txt = []
    for tic in x_axis["tics"]:
        txt.append(
            text(
                scale(tic, x_axis) - 4,
                y_scale(y_axis["min"], y_axis) + 18,
                "%s" % tic
            )
        )

    return txt


def x_axis_title(x_axis, y_axis):
    x = ((x_axis["max"] - x_axis["min"]) / 2) + x_axis["min"]
    return [
        text(
            scale(x, x_axis) - (len(x_axis["title"]) * 6),
            y_scale(y_axis["min"], y_axis) + 34,
            x_axis["title"],
            style="font: 18px sans-serif"
        )
    ]


def y_axis_lines(x_axis, y_axis):
    lines = []
    for tic in y_axis["tics"]:
        y = y_scale(tic, y_axis)
        lines.append(
            line(
                scale(x_axis["min"], x_axis),
                y,
                scale(x_axis["max"], x_axis),
                y,
                opacity=0.5,
                dashes=3
            )
        )

    return lines


def y_axis_tics(x_axis, y_axis, side):
    if side == "left":
        x1 = scale(x_axis["min"], x_axis) - 6
        x2 = scale(x_axis["min"], x_axis)
    else:
        x1 = scale(x_axis["max"], x_axis)
        x2 = scale(x_axis["max"], x_axis) + 4

    tics = [
        line(
            scale(x_axis["min"], x_axis),
            y_scale(y_axis["min"], y_axis),
            scale(x_axis["max"], x_axis),
            y_scale(y_axis["min"], y_axis)
        )
    ]
    for tic in y_axis["tics"]:
        tics.append(
            line(
                x1,
                y_scale(tic, y_axis),
                x2,
                y_scale(tic, y_axis)
            )
        )

    return tics


def zeroes(value, result=1):
    if value < 10:
        return result
    else:
        return zeroes(value/10, result=result+1)


def y_axis_text(x_axis, y_axis, side):
    if side == "left":
        x = scale(x_axis["min"], x_axis) - 8
    else:
        x = scale(x_axis["max"], x_axis) + 6
    txt = []
    for tic in y_axis["tics"]:
        z = zeroes(tic)
        r = x
        if side == "left":
            r = x - (z * 8)
        txt.append(
            text(r, y_scale(tic, y_axis) + 3, "%s" % tic)
        )

    return txt


def y_axis_title(x_axis, y_axis, side):
    if side == "left":
        y = 45
        x = -(y_scale(y_axis["min"], y_axis))
        transform = "rotate(270)"
    else:
        y = -35 - scale(x_axis["max"], x_axis)
        x = y_scale(y_axis["max"], y_axis)
        transform = "rotate(90)"
    return [
        text(
            x,
            y,
            y_axis["title"],
            style="font: 18px sans-serif",
            transform=transform
        )
    ]


def title(txt, x_axis):
    return [
        text(
            scale(x_axis["min"], x_axis),
            30,
            txt,
            style="font: 22px sans-serif",
        )
    ]


def get_keys(key_items, x_axis, y_axis, element_type="line"):
    keys = []
    x = scale(x_axis["max"], x_axis) + 60
    y = y_scale(y_axis["max"], y_axis)

    for idx, key in enumerate(key_items):
        color = color_arr[idx % len(color_arr)]
        y_val = y + (15 * (idx + 1))
        keys.append(get_key_symbol(x, y_val, element_type, color))
        keys.append(text(x + 20, y_val, key))

    return keys


def get_key_symbol(x, y, element_type, color):
    return {
        "line": line(x, y - 6, x + 15, y - 6, color=color, thickness=3),
        "circle": circle(x + 10, y - 4, 4, fill_color=color, border_color=color),
        "rect": rect(x + 6, y - 8, 8, 8, fill_color=color),
    }[element_type]


def add_chart_to_page(page, chart):
    if page.value is None:
        page.value = [chart]
    else:
        page.value.append(chart)
    return page

from charts.colors import color_arr
from charts.scale import x_scale, y_scale


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
        x = x_scale(tic, x_axis)
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
            x_scale(x_axis["tics"][0], x_axis),
            y_scale(y_axis["min"], y_axis),
            x_scale(x_axis["tics"][0], x_axis),
            y_scale(y_axis["max"], y_axis)
        )
    ]

    for tic in x_axis["tics"]:
        tics.append(
            line(
                x_scale(tic, x_axis),
                y_scale(y_axis["min"], y_axis),
                x_scale(tic, x_axis),
                y_scale(y_axis["min"], y_axis) + 6
            )
        )

    return tics


def x_axis_text(x_axis, y_axis):
    txt = []
    for tic in x_axis["tics"]:
        txt.append(
            text(
                x_scale(tic, x_axis) - 4,
                y_scale(y_axis["min"], y_axis) + 18,
                "%s" % tic
            )
        )

    return txt


def x_axis_title(x_axis, y_axis):
    x = ((x_axis["max"] - x_axis["min"]) / 2) + x_axis["min"]
    return [
        text(
            x_scale(x, x_axis) - (len(x_axis["title"]) * 6),
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
                x_scale(x_axis["min"], x_axis),
                y,
                x_scale(x_axis["max"], x_axis),
                y,
                opacity=0.5,
                dashes=3
            )
        )

    return lines


def y_axis_tics(x_axis, y_axis):
    tics = [
        line(
            x_scale(x_axis["min"], x_axis),
            y_scale(y_axis["min"], y_axis),
            x_scale(x_axis["max"], x_axis),
            y_scale(y_axis["min"], y_axis)
        )
    ]
    for tic in y_axis["tics"]:
        tics.append(
            line(
                x_scale(x_axis["min"], x_axis) - 6,
                y_scale(tic, y_axis),
                x_scale(x_axis["min"], x_axis),
                y_scale(tic, y_axis)
            )
        )

    return tics


def y_axis_text(x_axis, y_axis):
    txt = []
    for tic in y_axis["tics"]:
        txt.append(
            text(
                x_scale(x_axis["min"], x_axis) - 30,
                y_scale(tic, y_axis) + 3,
                "%s" % tic
            )
        )

    return txt


def y_axis_title(y_axis):
    return [
        text(
            -(y_scale(y_axis["min"], y_axis)),
            30,
            y_axis["title"],
            style="font: 18px sans-serif",
            transform="rotate(270)"
        )
    ]


def title(txt, x_axis):
    return [
        text(
            x_scale(x_axis["min"], x_axis),
            30,
            txt,
            style="font: 22px sans-serif",
        )
    ]


def get_keys(key_items, x_axis, y_axis, element_type="line"):
    keys = []
    x = x_scale(x_axis["max"], x_axis) + 5
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

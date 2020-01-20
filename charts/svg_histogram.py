import charts.svg as svg
from charts.scale import x_scale, y_scale


def get_svg(pop_data, sample_data, x_axis, y_axis, col="Total_CN_raw"):
    chart = svg.headers()

    svg_lines = []
    svg_lines += x_axis_lines(x_axis, y_axis)
    svg_lines += x_axis_tics(x_axis, y_axis)
    svg_lines += y_axis_lines(x_axis, y_axis)
    svg_lines += y_axis_tics(x_axis, y_axis)
    svg_lines += x_axis_text(x_axis, y_axis)
    svg_lines += x_axis_title(x_axis, y_axis)
    svg_lines += y_axis_text(x_axis, y_axis)
    svg_lines += y_axis_title(y_axis)
    svg_lines += histogram_lines(pop_data, x_axis, y_axis)
    svg_lines += sample_lines(sample_data, x_axis, y_axis)
    svg_lines += title("%s" % col, x_axis)

    chart.value = svg_lines
    return chart


def histogram_lines(pop_data, x_axis, y_axis):
    histo_lines = []
    for cn in pop_data:
        y = y_scale(pop_data[cn], y_axis)
        x = x_scale(cn, x_axis)
        histo_lines.append(
            svg.line(
                x,
                y,
                x,
                y_scale(0, y_axis),
                color="#646464",
                opacity=0.5
            )
        )
    return histo_lines


def sample_lines(sample_data, x_axis, y_axis):
    lines = []
    for idx, key in enumerate(sample_data.keys()):
        x = x_scale(sample_data[key], x_axis)
        lines.append(
            svg.line(
                x,
                y_scale(0, y_axis),
                x,
                y_scale(y_axis["max"], y_axis),
                color="blue"
            )
        )

    return lines


def x_axis_lines(x_axis, y_axis):
    lines = []
    for tic in x_axis["tics"]:
        x = x_scale(tic, x_axis)
        lines.append(
            svg.line(
                x,
                y_scale(0, y_axis),
                x,
                y_scale(y_axis["max"], y_axis),
                opacity=0.5,
                dashes=3
            )
        )

    return lines


def x_axis_tics(x_axis, y_axis):
    tics = [
        svg.line(
            x_scale(x_axis["tics"][0], x_axis),
            y_scale(0, y_axis),
            x_scale(x_axis["tics"][0], x_axis),
            y_scale(y_axis["max"], y_axis)
        )
    ]

    for tic in x_axis["tics"]:
        tics.append(
            svg.line(
                x_scale(tic, x_axis),
                y_scale(y_axis["min"], y_axis),
                x_scale(tic, x_axis),
                y_scale(y_axis["min"], y_axis) + 6
            )
        )

    return tics


def x_axis_text(x_axis, y_axis):
    text = []
    for tic in x_axis["tics"]:
        text.append(
            svg.text(
                x_scale(tic, x_axis) - 4,
                y_scale(y_axis["min"], y_axis) + 18,
                "%s" % tic
            )
        )

    return text


def x_axis_title(x_axis, y_axis):
    x = ((x_axis["max"] - x_axis["min"]) / 2) + x_axis["min"]
    return [
        svg.text(
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
            svg.line(
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
        svg.line(
            x_scale(x_axis["min"], x_axis),
            y_scale(y_axis["min"], y_axis),
            x_scale(x_axis["max"], x_axis),
            y_scale(y_axis["min"], y_axis)
        )
    ]
    for tic in y_axis["tics"]:
        tics.append(
            svg.line(
                x_scale(x_axis["min"], x_axis) - 6,
                y_scale(tic, y_axis),
                x_scale(x_axis["min"], x_axis),
                y_scale(tic, y_axis)
            )
        )

    return tics


def y_axis_text(x_axis, y_axis):
    text = []
    for tic in y_axis["tics"]:
        text.append(
            svg.text(
                x_scale(x_axis["min"], x_axis) - 30,
                y_scale(tic, y_axis) + 3,
                "%s" % tic
            )
        )

    return text


def y_axis_title(y_axis):
    return [
        svg.text(
            -(y_scale(y_axis["min"], y_axis)),
            30,
            y_axis["title"],
            style="font: 18px sans-serif",
            transform="rotate(270)"
        )
    ]


def title(txt, x_axis):
    return [
        svg.text(
            x_scale(x_axis["min"], x_axis),
            30,
            txt,
            style="font: 22px sans-serif",
        )
    ]

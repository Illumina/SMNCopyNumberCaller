import math

import charts.svg as svg


def get_svg(pop_data_file, sample_file, col="Total_CN_raw", padding=40, width=600, height=300):
    pop_data = read_pop_data(pop_data_file, col=col)
    sample_data = read_sample_data(sample_file, col=col)
    x_axis = get_x_axis(pop_data, width, padding)
    y_axis = get_y_axis(pop_data, height, padding)

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

    return svg_lines


def add_to_map(data_map, key):
    if key in data_map:
        data_map[key] += 1
    elif key not in data_map:
        data_map[key] = 1

    return data_map


def read_pop_data(data_file, col="Total_CN_raw"):
    data_map = {}

    with open(data_file) as fi:
        first = True

        for line in fi:
            spl = line.split('\t')
            idx = 6

            if first:
                first = False
                for i, column in enumerate(spl):
                    if column == col:
                        idx = i
            else:
                cn = round(float(spl[idx]), 2)
                data_map = add_to_map(data_map, cn)

    return data_map


def read_sample_data(sample_file, col):
    sample_map = {}
    first = True

    with open(sample_file, 'r') as fi:

        for line in fi:
            spl = line.split('\t')
            idx = 6

            if first:
                first = False
                for i, column in enumerate(spl):
                    if column == col:
                        idx = i

            else:
                sample = spl[0]
                cn = round(float(spl[idx]), 2)
                sample_map[sample] = cn

    return sample_map


def get_x_axis(pop_data, width, padding):
    minimum = math.floor(min(pop_data.keys()))
    maximum = round(max(pop_data.keys()))

    return {
        "min": minimum,
        "max": maximum,
        "tics": range(minimum, maximum),
        "title": "Copy Number",
        "domain": [padding, width - padding]
    }


def get_y_axis(pop_data, height, padding):
    minimum = 0
    maximum = round(max(pop_data.values()))

    return {
        "min": minimum,
        "max": maximum,
        "tics": range(minimum, maximum, 20),
        "title": "Sample Count",
        "domain": [padding, height - padding]
    }


def scale(val, axis):
    domain_diff = axis["domain"][1] - axis["domain"][0]
    range_diff = axis["max"] - axis["min"]
    x_offset = val - axis["min"]
    return ((x_offset / range_diff) * domain_diff) + axis["domain"][0]


def x_scale(val, axis):
    return axis["domain"][0] + scale(val, axis)


def y_scale(val, axis):
    return axis["domain"][0] + axis["domain"][1] - scale(val, axis)


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
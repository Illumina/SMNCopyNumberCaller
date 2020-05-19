import math

import charts.scale as scale
import charts.svgs.svg_line_chart as svg_line
import charts.pdfs.pdf_line_chart as pdf_line


class LineConfigException(Exception):
    pass


def get_line_chart(group, config, col, fmt):
    width = config["width"]
    height = config["height"]
    padding = config["padding"]

    x_axis = get_line_x_axis(group, width, padding)
    y_axis = get_line_y_axis(group, height, padding)

    if fmt == "svg":
        return svg_line.get_svg(group, config, x_axis, y_axis, col=col)
    elif fmt == "pdf":
        return pdf_line.get_pdf(group, x_axis, y_axis, col=col)


def get_line_x_axis(data, width, padding):
    sam = next(iter(data))
    minimum = min([x[0] for x in data[sam]]) - 1
    maximum = max([x[0] for x in data[sam]]) + 1
    return scale.axis(
        [minimum, maximum],
        [padding, width - padding],
        "Site Number",
        tic_values=[x for x in range(minimum + 1, maximum)]
    )


def get_line_y_axis(data, height, padding):
    max_val = None
    min_val = None
    for sample_id in data:
        sample_min = min([x[1] for x in data[sample_id]]) - 1
        sample_max = max([x[1] for x in data[sample_id]]) + 1

        if max_val is None or max_val < sample_max:
            max_val = sample_max
        if min_val is None or min_val > sample_min:
            min_val = sample_min

    if min_val < 0:
        min_val = 0

    return scale.axis([math.floor(min_val), math.ceil(max_val)], [padding, height - padding], "Raw CN", tics=6)

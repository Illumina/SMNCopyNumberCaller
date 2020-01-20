import json
import math

import charts.svg_line_chart as svg_line
from functools import reduce


class LineConfigException(Exception):
    pass


def get_line_chart(config, col, idx):
    width = config["line_charts"]["width"]
    height = config["line_charts"]["height"]
    padding = config["line_charts"]["padding"]

    sample_data = read_sample_line_data(config["sample_file"], col=col)

    x_axis = get_line_x_axis(sample_data, width, padding)
    y_axis = get_line_y_axis(sample_data, height, padding)

    chart = svg_line.get_svg(sample_data, x_axis, y_axis, col=col)
    chart.add_attr(["x", "0"])
    chart.add_attr(["y", "%s" % (idx * (config["height"] + config["padding"]))])
    return chart


def read_sample_line_data(file_in, col="SMN1_CN_raw"):
    sample_data = {}
    with open(file_in, 'r') as fi:
        samples = json.load(fi)
        for key in samples:
            sample_data[key] = samples[key][col]

    return sample_data


def get_line_x_axis(sample_data, width, padding):
    sam = next(iter(sample_data))
    return {
        "min": 1,
        "max": len(sample_data[sam]),
        "tics": range(1, len(sample_data[sam]) + 1),
        "title": "Site Number",
        "domain": [padding, width - padding]
    }


def get_line_y_axis(sample_data, height, padding):
    max_val = None
    min_val = None
    for sample_id in sample_data:
        sample_max = reduce(lambda a, b: max(a, b), sample_data[sample_id])
        sample_min = reduce(lambda a, b: min(a, b), sample_data[sample_id])

        if max_val is None or max_val < sample_max:
            max_val = sample_max
        if min_val is None or min_val > sample_min:
            min_val = sample_min

    return {
        "min": math.floor(min_val),
        "max": math.ceil(max_val),
        "tics": range(math.floor(min_val), math.ceil(max_val)),
        "title": "Raw SMN CN",
        "domain": [padding, height - padding]
    }

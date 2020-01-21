import math
import charts.svg_histogram as svg_histo


class ConfigException(Exception):
    pass


def get_histogram(pop_data, sample_data, config, col, idx):
    width = config["width"]
    height = config["height"]
    padding = config["padding"]

    x_axis = get_x_axis(pop_data, width, padding)
    y_axis = get_y_axis(pop_data, height, padding)

    histogram = svg_histo.get_svg(pop_data, sample_data, x_axis, y_axis, col=col)
    histogram.add_attr(["x", "0"])
    histogram.add_attr(["y", "%s" % (idx * (height + padding))])
    return histogram


def add_to_map(data_map, key):
    if key in data_map:
        data_map[key] += 1
    elif key not in data_map:
        data_map[key] = 1

    return data_map


def get_x_axis(pop_data, width, padding):
    minimum = math.floor(min(pop_data.keys()))
    maximum = math.ceil(max(pop_data.keys())) + 1

    return {
        "min": minimum,
        "max": maximum,
        "tics": range(minimum, maximum),
        "title": "Copy Number",
        "domain": [padding, width - padding]
    }


def get_y_axis(pop_data, height, padding):
    minimum = 0
    maximum = math.ceil(max(pop_data.values())) + 1

    return {
        "min": minimum,
        "max": maximum,
        "tics": range(minimum, maximum, 20),
        "title": "Sample Count",
        "domain": [padding, height - padding]
    }

import math
import charts.svg_histogram as svg_histo
import json


class ConfigException(Exception):
    pass


def get_histogram(config, col, idx):
    width = config["histograms"]["width"]
    height = config["histograms"]["height"]
    padding = config["histograms"]["padding"]

    pop_data = read_pop_data(config["pop_file"], col=col)
    sample_data = read_sample_data(config["sample_file"], col=col)

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

    with open(sample_file, 'r') as fi:
        samples = json.load(fi)
        for key in samples:
            try:
                sample_map[key] = round(float(samples[key][col]), 2)
            except Exception as e:
                raise ConfigException("Invalid column key or value. "
                                      "Check config is correct and json has a value for every sample: %s" % e)

    return sample_map


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

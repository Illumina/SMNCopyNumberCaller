import math
import charts.svgs.svg_histogram as svg_histo
import charts.pdfs.pdf_histogram as pdf_histo
import charts.scale as scale


class ConfigException(Exception):
    pass


def get_histogram(pop_data, sample_data, config, col, fmt):
    width = config["width"]
    height = config["height"]
    padding = config["padding"]

    x_axis = get_x_axis(pop_data, width, padding)
    y_axis = get_y_axis(pop_data, height, padding)

    if fmt == "svg":
        return svg_histo.get_svg(pop_data, sample_data, config, x_axis, y_axis, col=col)
    elif fmt == "pdf":
        return pdf_histo.get_pdf(pop_data, sample_data, config, x_axis, y_axis, col=col)


def add_to_map(data_map, key):
    if key in data_map:
        data_map[key] += 1
    elif key not in data_map:
        data_map[key] = 1

    return data_map


def get_x_axis(pop_data, width, padding):
    minimum = 0
    maximum = math.ceil(max(pop_data.keys())) + 1

    return scale.axis([minimum, maximum], [padding, width - padding], "Copy Number", tics=8)


def get_y_axis(pop_data, height, padding):
    minimum = 0
    maximum = math.ceil(max(pop_data.values())) + 1

    return scale.axis([minimum, maximum], [padding, height - padding], "Sample Count")

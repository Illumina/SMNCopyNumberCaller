import math

letter = [8.5, 11]
letter_points = [p * 72 for p in letter]


def _scale(val, axes):
    domain_diff = axes["domain"][1] - axes["domain"][0]
    range_diff = axes["max"] - axes["min"]
    x_offset = val - axes["min"]
    return ((x_offset / range_diff) * domain_diff) + axes["domain"][0]


def pdf_scale(conf):
    ratio = letter_points[1] / (conf["set_width"] + 600)
    conf["height"] = ratio * conf["set_height"]
    conf["width"] = ratio * conf["set_width"]
    conf["padding"] = ratio * conf["set_padding"]
    return conf


def scale(val, axes):
    return axes["domain"][0] + _scale(val, axes)


def y_scale(val, axes):
    return axes["domain"][0] + axes["domain"][1] - _scale(val, axes)


def axis(data_range, coord_range, title, tics=5, tic_values=None):
    if tic_values is not None:
        tics = tic_values
    else:
        tic_step = math.ceil((data_range[1] - data_range[0]) / tics)
        tics = range(math.floor(data_range[0]), math.ceil(data_range[1] + 1), tic_step)

    return {
        "min": data_range[0],
        "max": data_range[1],
        "tics": tics,
        "title": title,
        "domain": [coord_range[0], coord_range[1]]
    }

letter = [8.5, 11]
letter_points = [p * 72 for p in letter]


def _scale(val, axis):
    domain_diff = axis["domain"][1] - axis["domain"][0]
    range_diff = axis["max"] - axis["min"]
    x_offset = val - axis["min"]
    return ((x_offset / range_diff) * domain_diff) + axis["domain"][0]


def pdf_scale(conf):
    ratio = letter_points[1] / (conf["width"] + 600)
    conf["height"] = ratio * conf["height"]
    conf["width"] = ratio * conf["width"]
    conf["padding"] = ratio * conf["padding"]
    return conf


def scale(val, axis):
    return axis["domain"][0] + _scale(val, axis)


def y_scale(val, axis):
    return axis["domain"][0] + axis["domain"][1] - _scale(val, axis)

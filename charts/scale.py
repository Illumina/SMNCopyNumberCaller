def scale(val, axis):
    domain_diff = axis["domain"][1] - axis["domain"][0]
    range_diff = axis["max"] - axis["min"]
    x_offset = val - axis["min"]
    return ((x_offset / range_diff) * domain_diff) + axis["domain"][0]


def x_scale(val, axis):
    return axis["domain"][0] + scale(val, axis)


def y_scale(val, axis):
    return axis["domain"][0] + axis["domain"][1] - scale(val, axis)
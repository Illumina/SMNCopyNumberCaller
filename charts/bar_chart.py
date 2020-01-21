import charts.svg_bar as svg_bar
import math


def get_bar_chart(conf, sample_data, idx):
    width = conf["width"]
    height = conf["height"]
    padding = conf["padding"]
    cols = conf["bar_charts"]["columns"]

    x_axis = get_bar_x_axis(sample_data, cols, width, padding)
    y_axis = get_bar_y_axis(sample_data, cols, height, padding)
    norm_y_axis = get_normalised_y_axis(sample_data, cols, height, padding)

    chart = svg_bar.get_svg(sample_data, x_axis, y_axis, norm_y_axis, cols)

    chart.add_attr(["x", "0"])
    chart.add_attr(["y", "%s" % (idx * (height + padding))])
    return chart


def get_bar_x_axis(sample_data, cols, width, padding):
    length = len(sample_data[cols[0]])
    for col in cols:
        assert len(sample_data[col]) == length

    return {
        "min": 0,
        "max": length + 1,
        "tics": range(0, length + 1),
        "title": "Site Number",
        "domain": [padding, width - padding]
    }


def get_bar_y_axis(sample_data, cols, height, padding):
    max_val = math.ceil(max(sample_data[cols[0]] + sample_data[cols[1]]))
    min_val = math.floor(min(sample_data[cols[0]] + sample_data[cols[1]]))
    return {
        "min": min_val,
        "max": max_val,
        "tics": range(min_val, max_val + 1, 10),
        "title": "Read Count",
        "domain": [padding, height - padding]
    }


def get_normalised_y_axis(sample_data, cols, height, padding):
    hap = sample_data["Median_depth"] / 2
    all_data = sample_data[cols[0]] + sample_data[cols[1]]
    mapped_data = [(x / hap) for x in all_data]
    max_val = math.ceil(max(mapped_data))
    min_val = math.floor(min(mapped_data))

    return {
        "min": min_val,
        "max": max_val,
        "tics": range(min_val, max_val + 1),
        "title": "Read Count",
        "domain": [padding, height - padding]
    }

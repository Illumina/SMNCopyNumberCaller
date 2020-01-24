import math

import charts.svgs.svg as svg
from charts.scale import scale, y_scale
from charts.colors import colors, color_arr


def get_svg(sample, conf, x_axis, y_axis, norm_y_axis, cols):
    chart = svg.headers()
    title = "%s: (SMN1: %s, SMN2: %s)" % (sample["sample"], sample["SMN1"], sample["SMN2"])

    svg_bars = []
    svg_bars += svg.x_axis_lines(x_axis, y_axis)
    svg_bars += svg.x_axis_tics(x_axis, y_axis)
    svg_bars += svg.x_axis_text(x_axis, y_axis)
    svg_bars += svg.x_axis_title(x_axis, y_axis)
    svg_bars += svg.y_axis_lines(x_axis, norm_y_axis)
    svg_bars += svg.y_axis_tics(x_axis, norm_y_axis, "left")
    svg_bars += svg.y_axis_text(x_axis, norm_y_axis, "left")
    svg_bars += svg.y_axis_title(x_axis, norm_y_axis, "left")
    svg_bars += svg.y_axis_tics(x_axis, y_axis, "right")
    svg_bars += svg.y_axis_text(x_axis, y_axis, "right")
    svg_bars += svg.y_axis_title(x_axis, y_axis, "right")
    svg_bars += svg.right_axis_line(x_axis, y_axis)
    svg_bars += sample_bars(sample, x_axis, norm_y_axis, cols)
    svg_bars += svg.title(title, x_axis)
    svg_bars += svg.get_keys(cols, x_axis, y_axis, element_type="rect")

    chart.value = svg_bars
    chart.add_attr(["x", "0"])
    chart.add_attr(["y", "%s" % (conf["index"] * (conf["height"] + conf["padding"]))])
    return chart


def sample_bars(sample_data, x_axis, y_axis, cols):
    hap = sample_data["Median_depth"] / 2
    smn1 = [(x[0], x[1] / hap) for x in sample_data[cols[0]]]
    smn2 = [(x[0], x[1] / hap) for x in sample_data[cols[1]]]

    bars = []
    for x_val, y_val in smn1:
        smn1_bar = get_bar(x_val - 0.4, y_val, x_axis, y_axis, color_arr[0])
        bars += [smn1_bar]
    for x_val, y_val in smn2:
        smn2_bar = get_bar(x_val, y_val, x_axis, y_axis, color_arr[1])
        bars += [smn2_bar]

    return bars


def get_bar(i, val, x_axis, y_axis, color):
    width = scale(2, x_axis) - scale(1.6, x_axis)
    y = y_scale(val, y_axis)
    height = y_scale(y_axis["min"], y_axis) - y
    x = scale(i, x_axis)
    return svg.rect(x, y, width, height, border_color=color, fill_color=color, opacity=0.7)

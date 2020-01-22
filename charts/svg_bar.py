import charts.svg as svg
from charts.scale import x_scale, y_scale
from charts.colors import colors, color_arr


def get_svg(sample_data, x_axis, y_axis, norm_y_axis, cols):
    chart = svg.headers()

    svg_bars = []
    svg_bars += svg.x_axis_lines(x_axis, y_axis)
    svg_bars += svg.x_axis_tics(x_axis, y_axis)
    svg_bars += svg.y_axis_lines(x_axis, y_axis)
    svg_bars += svg.y_axis_tics(x_axis, y_axis)
    svg_bars += svg.x_axis_text(x_axis, y_axis)
    svg_bars += svg.x_axis_title(x_axis, y_axis)
    svg_bars += svg.y_axis_text(x_axis, y_axis)
    svg_bars += svg.y_axis_title(y_axis)
    svg_bars += sample_bars(sample_data, x_axis, y_axis, cols)
    svg_bars += sample_lines(sample_data, x_axis, norm_y_axis, cols)
    svg_bars += svg.title(sample_data["sample"], x_axis)
    svg_bars += svg.get_keys(cols, x_axis, y_axis, element_type="rect")

    chart.value = svg_bars
    return chart


def sample_bars(sample_data, x_axis, y_axis, cols):
    smn1 = sample_data[cols[0]]
    smn2 = sample_data[cols[1]]

    bars = []
    for i in range(0, len(smn1)):
        smn1_bar = get_bar(i + 0.6, smn1[i], x_axis, y_axis, color_arr[0])
        smn2_bar = get_bar(i + 1, smn2[i], x_axis, y_axis, color_arr[1])
        bars += [smn1_bar, smn2_bar]

    return bars


def sample_lines(sample_data, x_axis, y_axis, cols):
    hap = sample_data["Median_depth"] / 2
    smn1 = [(v / hap) for v in sample_data[cols[0]]]
    smn2 = [(v / hap) for v in sample_data[cols[1]]]

    smn1_points = []
    smn2_points = []
    for i in range(0, len(smn1)):
        smn1_points.append("%s,%s" % (x_scale(i + 0.8, x_axis), y_scale(smn1[i], y_axis)))
        smn2_points.append("%s,%s" % (x_scale(i + 1.2, x_axis), y_scale(smn2[i], y_axis)))

    smn1_line = svg.path(smn1_points, color=color_arr[0])
    smn2_line = svg.path(smn2_points, color=color_arr[1])

    return [smn1_line, smn2_line]


def get_bar(i, val, x_axis, y_axis, color):
    width = x_scale(2, x_axis) - x_scale(1.6, x_axis)
    y = y_scale(val, y_axis)
    height = y_scale(y_axis["min"], y_axis) - y
    x = x_scale(i, x_axis)
    return svg.rect(x, y, width, height, border_color=colors["grey"], fill_color=color, opacity=0.7)

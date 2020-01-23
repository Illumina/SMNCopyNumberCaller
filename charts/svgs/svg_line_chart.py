import charts.svgs.svg as svg
from charts.scale import scale, y_scale
from charts.colors import color_arr


def get_svg(sample_data, config, x_axis, y_axis, col="SMN1_CN_raw"):
    line_chart = svg.headers()

    svg_lines = []
    svg_lines += svg.x_axis_lines(x_axis, y_axis)
    svg_lines += svg.x_axis_tics(x_axis, y_axis)
    svg_lines += svg.x_axis_text(x_axis, y_axis)
    svg_lines += svg.x_axis_title(x_axis, y_axis)
    svg_lines += svg.y_axis_lines(x_axis, y_axis)
    svg_lines += svg.y_axis_tics(x_axis, y_axis, "left")
    svg_lines += svg.y_axis_text(x_axis, y_axis, "left")
    svg_lines += svg.y_axis_title(x_axis, y_axis, "left")
    svg_lines += sample_paths(sample_data, x_axis, y_axis)
    svg_lines += circles(sample_data, x_axis, y_axis)
    svg_lines += svg.title("%s" % col, x_axis)
    svg_lines += svg.get_keys([key for key in sample_data], x_axis, y_axis, element_type="circle")

    line_chart.value = svg_lines
    line_chart.add_attr(["x", "0"])
    line_chart.add_attr(["y", "%s" % (config["index"] * (config["height"] + config["padding"]))])
    return line_chart


def sample_paths(sample_data, x_axis, y_axis):
    paths = []
    for idx, sample in enumerate(sample_data):
        points = []
        for x_idx, value in enumerate(sample_data[sample]):
            points.append("%s,%s" % (scale(value[0], x_axis), y_scale(value[1], y_axis)))
        color = color_arr[idx % len(color_arr)]
        paths.append(svg.path(points, color=color))

    return paths


def circles(sample_data, x_axis, y_axis):
    spots = []

    for idx, sample in enumerate(sample_data):
        colour = color_arr[idx % len(color_arr)]
        for x_val, y_val in sample_data[sample]:
            circle = svg.circle(
                    scale(x_val, x_axis),
                    y_scale(y_val, y_axis),
                    4,
                    fill_color=colour,
                    border_color=colour
                )
            circle = svg.add_tooltip(circle, "Sample: %s\nSite: %s\nValue: %s" % (sample, x_val + 1, y_val))
            spots.append(circle)
    return spots

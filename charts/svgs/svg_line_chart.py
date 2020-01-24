import charts.svgs.svg as svg
from charts.scale import scale, y_scale
from charts.colors import color_arr


def get_svg(data, config, x_axis, y_axis, col="SMN1_CN_raw"):
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
    svg_lines += sample_paths(data, x_axis, y_axis)

    svg_lines += circles(data, x_axis, y_axis)
    svg_lines += svg.title("%s" % col, x_axis)
    svg_lines += svg.get_keys([key for key in data], x_axis, y_axis, element_type="circle")

    line_chart.value = svg_lines
    line_chart.add_attr(["x", "0"])
    line_chart.add_attr(["y", "%s" % (config["index"] * (config["height"] + config["padding"]))])
    return line_chart


def sample_paths(data, x_axis, y_axis):
    paths = []
    for idx, key in enumerate(data):
        points = []
        for x_idx, value in enumerate(data[key]):
            points.append("%s,%s" % (scale(value[0], x_axis), y_scale(value[1], y_axis)))
        color = color_arr[idx % len(color_arr)]
        paths.append(svg.path(points, color=color))

    return paths


def circles(data, x_axis, y_axis):
    spots = []

    for idx, group in enumerate(data):
        colour = color_arr[idx % len(color_arr)]
        for x_val, y_val in data[group]:
            circle = svg.circle(
                    scale(x_val, x_axis),
                    y_scale(y_val, y_axis),
                    4,
                    fill_color=colour,
                    border_color=colour
                )
            circle = svg.add_tooltip(circle, "%s\n%s: %s\nValue: %s" % (group, x_axis["title"], x_val + 1, y_val))
            spots.append(circle)
    return spots

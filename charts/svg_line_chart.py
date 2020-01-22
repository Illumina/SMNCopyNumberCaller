import charts.svg as svg
from charts.scale import x_scale, y_scale
from charts.colors import color_arr


def get_svg(sample_data, x_axis, y_axis, col="SMN1_CN_raw"):
    line_chart = svg.headers()

    svg_lines = []
    svg_lines += svg.x_axis_lines(x_axis, y_axis)
    svg_lines += svg.x_axis_tics(x_axis, y_axis)
    svg_lines += svg.y_axis_lines(x_axis, y_axis)
    svg_lines += svg.y_axis_tics(x_axis, y_axis)
    svg_lines += svg.x_axis_text(x_axis, y_axis)
    svg_lines += svg.x_axis_title(x_axis, y_axis)
    svg_lines += svg.y_axis_text(x_axis, y_axis)
    svg_lines += svg.y_axis_title(y_axis)
    svg_lines += sample_paths(sample_data, x_axis, y_axis)
    svg_lines += circles(sample_data, x_axis, y_axis)
    svg_lines += svg.title("%s" % col, x_axis)
    svg_lines += svg.get_keys([key for key in sample_data], x_axis, y_axis, element_type="circle")

    line_chart.value = svg_lines
    return line_chart


def sample_paths(sample_data, x_axis, y_axis):
    paths = []
    for idx, sample in enumerate(sample_data):
        points = []
        for x_idx, value in enumerate(sample_data[sample]):
            points.append("%s,%s" % (x_scale(x_idx + 1, x_axis), y_scale(value, y_axis)))
        color = color_arr[idx % len(color_arr)]
        paths.append(svg.path(points, color=color))

    return paths


def circles(sample_data, x_axis, y_axis):
    spots = []
    for idx, sample in enumerate(sample_data):
        colour = color_arr[idx % len(color_arr)]
        for x_idx, value in enumerate(sample_data[sample]):
            circle = svg.circle(
                    x_scale(x_idx + 1, x_axis),
                    y_scale(value, y_axis),
                    3,
                    fill_color=colour,
                    border_color=colour
                )
            circle = svg.add_tooltip(circle, "Sample: %s\nSite: %s\nValue: %s" % (sample, x_idx + 1, value))
            spots.append(circle)
    return spots

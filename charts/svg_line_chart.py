import charts.svg as svg
from charts.scale import x_scale, y_scale


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

    line_chart.value = svg_lines
    return line_chart


def sample_paths(sample_data, x_axis, y_axis):
    paths = []
    colors = ["blue", "green", "orange", "black", "red", "pink"]
    for idx, sample in enumerate(sample_data):
        points = []
        for x_idx, value in enumerate(sample_data[sample]):
            points.append("%s,%s" % (x_scale(x_idx + 1, x_axis), y_scale(value, y_axis)))
        color = colors[idx % len(colors)]
        paths.append(svg.path(points, color=color))

    return paths


def circles(sample_data, x_axis, y_axis):
    spots = []
    colors = ["blue", "green", "orange", "black", "red", "pink"]
    for idx, sample in enumerate(sample_data):
        colour = colors[idx % 6]
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

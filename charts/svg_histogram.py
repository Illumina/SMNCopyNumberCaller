import charts.svg as svg
from charts.scale import x_scale, y_scale
from charts.colors import colors, color_arr


def get_svg(pop_data, sample_data, x_axis, y_axis, col="Total_CN_raw"):
    chart = svg.headers()

    svg_lines = []
    svg_lines += svg.x_axis_lines(x_axis, y_axis)
    svg_lines += svg.x_axis_tics(x_axis, y_axis)
    svg_lines += svg.y_axis_lines(x_axis, y_axis)
    svg_lines += svg.y_axis_tics(x_axis, y_axis)
    svg_lines += svg.x_axis_text(x_axis, y_axis)
    svg_lines += svg.x_axis_title(x_axis, y_axis)
    svg_lines += svg.y_axis_text(x_axis, y_axis)
    svg_lines += svg.y_axis_title(y_axis)
    svg_lines += histogram_lines(pop_data, x_axis, y_axis)
    svg_lines += sample_lines(sample_data, x_axis, y_axis)
    svg_lines += svg.title("%s" % col, x_axis)
    svg_lines += svg.get_keys([key for key in sample_data], x_axis, y_axis)

    chart.value = svg_lines
    return chart


def histogram_lines(pop_data, x_axis, y_axis):
    histo_lines = []
    for cn in pop_data:
        y = y_scale(pop_data[cn], y_axis)
        x = x_scale(cn, x_axis)
        histo_lines.append(
            svg.line(
                x,
                y,
                x,
                y_scale(0, y_axis),
                color=colors["grey"],
                opacity=0.5
            )
        )
    return histo_lines


def sample_lines(sample_data, x_axis, y_axis):
    lines = []
    samples = iter(sample_data)
    for idx, key in enumerate(samples):
        x = x_scale(sample_data[key], x_axis)
        lines.append(
            svg.line(
                x,
                y_scale(0, y_axis),
                x,
                y_scale(y_axis["max"], y_axis),
                color=color_arr[idx % len(color_arr)]
            )
        )

    return lines


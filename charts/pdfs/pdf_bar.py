import charts.pdfs.pdf as pdf
from charts.scale import scale, y_scale
from charts.colors import colors, color_arr


def get_pdf(sample_data, x_axis, y_axis, norm_y_axis, cols):

    pdf_bars = []
    pdf_bars += pdf.x_axis_lines(x_axis, y_axis)
    pdf_bars += pdf.x_axis_tics(x_axis, y_axis)
    pdf_bars += pdf.x_axis_text(x_axis, y_axis)
    pdf_bars += pdf.x_axis_title(x_axis, y_axis)
    pdf_bars += pdf.y_axis_lines(x_axis, y_axis)
    pdf_bars += pdf.y_axis_tics(x_axis, y_axis, "left")
    pdf_bars += pdf.y_axis_text(x_axis, y_axis, "left")
    pdf_bars += pdf.y_axis_title(x_axis, y_axis, "left")
    pdf_bars += pdf.y_axis_tics(x_axis, norm_y_axis, "right")
    pdf_bars += pdf.y_axis_text(x_axis, norm_y_axis, "right")
    pdf_bars += pdf.y_axis_title(x_axis, norm_y_axis, "right")
    pdf_bars += sample_bars(sample_data, x_axis, y_axis, cols)
    pdf_bars += sample_lines(sample_data, x_axis, norm_y_axis, cols)
    pdf_bars += pdf.title(sample_data["sample"], x_axis, y_axis)
    pdf_bars += pdf.get_keys(cols, x_axis, y_axis, element_type="rect")
    return pdf_bars


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
        smn1_points.append(scale(i + 0.8, x_axis))
        smn1_points.append(scale(smn1[i], y_axis))
        smn2_points.append(scale(i + 1.2, x_axis))
        smn2_points.append(scale(smn2[i], y_axis))

    smn1_line = pdf.path(smn1_points, color=color_arr[0])
    smn2_line = pdf.path(smn2_points, color=color_arr[1])

    return [smn1_line, smn2_line]


def get_bar(i, val, x_axis, y_axis, color):
    width = scale(2, x_axis) - scale(1.6, x_axis)
    y = scale(val, y_axis)
    height = scale(y_axis["min"], y_axis) - y
    x = scale(i, x_axis)
    return pdf.rect(x, y, width, height, border_color=colors["grey"], fill_color=color, opacity=0.6)

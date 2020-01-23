import charts.pdfs.pdf as pdf
from charts.colors import colors, color_arr
from charts.scale import scale
from reportlab.graphics.shapes import Line


def get_pdf(pop_data, sample_data, x_axis, y_axis, col="Total_CN_raw", header=None):
    pdf_items = []
    pdf_items += pdf.x_axis_lines(x_axis, y_axis)
    pdf_items += pdf.x_axis_tics(x_axis, y_axis)
    pdf_items += pdf.y_axis_lines(x_axis, y_axis)
    pdf_items += pdf.y_axis_tics(x_axis, y_axis, "left")
    pdf_items += pdf.x_axis_text(x_axis, y_axis)
    pdf_items += pdf.x_axis_title(x_axis, y_axis)
    pdf_items += pdf.y_axis_text(x_axis, y_axis, "left")
    pdf_items += pdf.y_axis_title(x_axis, y_axis, "left")
    pdf_items += histogram_lines(pop_data, x_axis, y_axis)
    pdf_items += sample_lines(sample_data, x_axis, y_axis)
    if header is not None:
        pdf_items += pdf.title("%s" % header, x_axis, y_axis)
    else:
        pdf_items += pdf.title("%s" % col, x_axis, y_axis)
    pdf_items += pdf.get_keys([key for key in sample_data], x_axis, y_axis)
    return pdf_items


def histogram_lines(pop_data, x_axis, y_axis):
    histo_lines = []
    for cn in pop_data:
        y = scale(pop_data[cn], y_axis)
        x = scale(cn, x_axis)
        histo_lines.append(
            Line(
                x,
                y,
                x,
                scale(0, y_axis),
                strokeColor=colors["grey"],
                strokeOpacity=0.3
            )
        )
    return histo_lines


def sample_lines(sample_data, x_axis, y_axis):
    lines = []
    samples = iter(sample_data)
    for idx, key in enumerate(samples):
        x = scale(sample_data[key], x_axis)
        lines.append(
            Line(
                x,
                scale(0, y_axis),
                x,
                scale(y_axis["max"], y_axis),
                strokeColor=color_arr[idx % len(color_arr)],
                strokeOpacity=1.0
            )
        )

    return lines

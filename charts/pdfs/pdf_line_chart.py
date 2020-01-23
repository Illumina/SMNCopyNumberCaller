from charts.colors import color_arr
from charts.pdfs import pdf
from charts.scale import scale
from reportlab.graphics.shapes import PolyLine


def get_pdf(sample_data, x_axis, y_axis, col="SMN1_CN_raw"):
    pdf_lines = []
    pdf_lines += pdf.x_axis_lines(x_axis, y_axis)
    pdf_lines += pdf.x_axis_tics(x_axis, y_axis)
    pdf_lines += pdf.y_axis_lines(x_axis, y_axis)
    pdf_lines += pdf.y_axis_tics(x_axis, y_axis, "left")
    pdf_lines += pdf.x_axis_text(x_axis, y_axis)
    pdf_lines += pdf.x_axis_title(x_axis, y_axis)
    pdf_lines += pdf.y_axis_text(x_axis, y_axis, "left")
    pdf_lines += pdf.y_axis_title(x_axis, y_axis, "left")
    pdf_lines += sample_paths(sample_data, x_axis, y_axis)
    pdf_lines += circles(sample_data, x_axis, y_axis)
    pdf_lines += pdf.title("%s" % col, x_axis, y_axis)
    pdf_lines += pdf.get_keys([key for key in sample_data], x_axis, y_axis, element_type="circle")

    return pdf_lines


def sample_paths(sample_data, x_axis, y_axis):
    paths = []
    for idx, sample in enumerate(sample_data):
        points = []
        for x_idx, value in enumerate(sample_data[sample]):
            points.append(scale(value[0], x_axis))
            points.append(scale(value[1], y_axis))

        color = color_arr[idx % len(color_arr)]
        paths.append(PolyLine(points, strokeColor=color, fillColor=color, strokeOpacity=1.0))

    return paths


def circles(sample_data, x_axis, y_axis):
    spots = []
    for idx, sample in enumerate(sample_data):
        colour = color_arr[idx % len(color_arr)]
        for x_idx, value in enumerate(sample_data[sample]):
            circle = pdf.circle(
                    scale(value[0], x_axis),
                    scale(value[1], y_axis),
                    3,
                    fill_color=colour,
                    border_color=colour
            )
            spots.append(circle)
    return spots

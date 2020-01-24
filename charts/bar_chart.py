import charts.svgs.svg_bar as svg_bar
import charts.pdfs.pdf_bar as pdf_bar
import charts.scale as scale
import math


def get_bar_chart(conf, sample_data, fmt):
    width = conf["width"]
    height = conf["height"]
    padding = conf["padding"]
    cols = conf["bar_charts"]["columns"]

    x_axis = get_bar_x_axis(sample_data, cols, width, padding)
    y_axis = get_bar_y_axis(sample_data, cols, height, padding)
    norm_y_axis = get_normalised_y_axis(sample_data, cols, height, padding)

    if fmt == "svg":
        return svg_bar.get_svg(sample_data, conf, x_axis, y_axis, norm_y_axis, cols)
    elif fmt == "pdf":
        return pdf_bar.get_pdf(sample_data, x_axis, y_axis, norm_y_axis, cols)


def get_bar_x_axis(sample_data, cols, width, padding):
    length = len(sample_data[cols[0]])
    for col in cols:
        assert len(sample_data[col]) == length

    data = [x[0] for x in sample_data[cols[0]]]
    x_min = min(data) - 1
    x_max = max(data) + 1

    return scale.axis(
        [x_min, x_max],
        [padding, width - padding],
        "Site Number",
        tic_values=[x for x in range(x_min + 1, x_max)]
    )


def get_bar_y_axis(sample_data, cols, height, padding):
    data = sample_data[cols[0]] + sample_data[cols[1]]
    max_val = math.ceil(max([x[1] for x in data]))

    return scale.axis([0, max_val], [padding, height - padding], "Read Count", tics=4)


def get_normalised_y_axis(sample_data, cols, height, padding):
    hap = sample_data["Median_depth"] / 2
    all_data = sample_data[cols[0]] + sample_data[cols[1]]
    mapped_data = [(x[1] / hap) for x in all_data]
    max_val = math.ceil(max(mapped_data))

    return scale.axis([0, max_val], [padding, height - padding], "Norm. Depth", tics=4)

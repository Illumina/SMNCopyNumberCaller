from reportlab.lib.pagesizes import letter
from charts.scale import pdf_scale
import charts.histogram as histo
import charts.svgs.svg as svg
import charts.line_chart as line_chart
import charts.bar_chart as bar_chart
import charts.data_utils as util
import charts.pdfs.pdf as pdf
from reportlab.graphics.shapes import Drawing
from reportlab.platypus import SimpleDocTemplate


def get_height(conf, sample_count):
    histo_height = len(conf["histograms"]["columns"]) * (conf["height"] + conf["padding"])
    lines_height = len(conf["line_charts"]["columns"]) * (conf["height"] + conf["padding"])
    bars_height = sample_count * (conf["height"] + conf["padding"])
    return histo_height + lines_height + bars_height


def svg_file(conf):
    return "%s/smn_charts.svg" % conf["output_dir"]


def png_file(conf):
    return "%s/smn_charts.png" % conf["output_dir"]


def pdf_file(conf):
    return "%s/smn_charts.pdf" % conf["output_dir"]


def write_pdf(conf, pop_data, sample_data):
    conf = pdf_scale(conf)
    page = SimpleDocTemplate(
        pdf_file(conf),
        pagesize=letter,
        leftMargin=0,
        rightMargin=0
    )

    elements = []

    for col in conf["histograms"]["columns"]:
        drawing = Drawing(conf["width"], conf["height"], vAlign="TOP")
        pop_col = util.get_pop_column(pop_data, col)
        sample_col_map = util.get_sample_col_map(sample_data, col)
        hist = histo.get_histogram(pop_col, sample_col_map, conf, col, "pdf")
        elements.append(pdf.add_chart_to_page(drawing, hist))

    for col in conf["line_charts"]["columns"]:
        drawing = Drawing(conf["width"], conf["height"], vAlign="TOP")
        sample_col_map = util.get_sample_col_map(sample_data, col)
        chart = line_chart.get_line_chart(sample_col_map, conf, col, "pdf")
        elements.append(pdf.add_chart_to_page(drawing, chart))

    for sample in sample_data:
        drawing = Drawing(conf["width"], conf["height"], vAlign="TOP")
        sam = sample_data[sample]
        sam["sample"] = sample
        bars = bar_chart.get_bar_chart(conf, sam, "pdf")
        elements.append(pdf.add_chart_to_page(drawing, bars))

    page.build(elements)


def write_svg(conf, pop_data, sample_data):
    height = get_height(conf, len(sample_data.keys()))
    page = svg.headers(height)
    idx = 0
    for col in conf["histograms"]["columns"]:
        conf["index"] = idx
        pop_col = util.get_pop_column(pop_data, col)
        sample_col_map = util.get_sample_col_map(sample_data, col)
        hist = histo.get_histogram(pop_col, sample_col_map, conf, col, "svg")
        idx += 1
        page = svg.add_chart_to_page(page, hist)

    for col in conf["line_charts"]["columns"]:
        conf["index"] = idx
        sample_col_map = util.get_sample_col_map(sample_data, col)
        chart = line_chart.get_line_chart(sample_col_map, conf, col, "svg")
        idx += 1
        page = svg.add_chart_to_page(page, chart)

    for sample in sample_data:
        conf["index"] = idx
        sam = sample_data[sample]
        sam["sample"] = sample
        bars = bar_chart.get_bar_chart(conf, sam, "svg")
        idx += 1
        page = svg.add_chart_to_page(page, bars)

    with open(svg_file(conf), 'w') as fo:
        fo.write(page.to_string())

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
    lines_height = sample_count * (conf["height"] + conf["padding"])
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
    chart_spacing = 50

    page = SimpleDocTemplate(
        pdf_file(conf),
        pagesize=letter,
        leftMargin=0,
        rightMargin=0
    )

    elements = []
    idx = 0

    def add_space():
        if idx == 0:
            return
        else:
            elements.append(Drawing(100, chart_spacing))

    for col in conf["histograms"]["columns"]:
        drawing = Drawing(conf["width"], conf["height"], vAlign="TOP")
        pop_col = util.get_pop_column(pop_data, col)
        sample_col_map = util.get_sample_col_map(sample_data, col)
        hist = histo.get_histogram(pop_col, sample_col_map, conf, col, "pdf")
        add_space()
        elements.append(pdf.add_chart_to_page(drawing, hist))
        idx += 1

    for sample in sample_data:
        drawing = Drawing(conf["width"], conf["height"], vAlign="TOP")
        col_map = util.get_key_map(conf["line_charts"]["columns"], sample_data[sample])
        cn = round(sample_data[sample]["Full_length_CN_raw"]) / 2
        col_map["SMN2_CN_raw"] = [(x[0], (cn - (x[1] - cn))) for x in col_map["SMN1_CN_raw"]]
        chart = line_chart.get_line_chart(col_map, conf, sample, "pdf")
        add_space()
        elements.append(pdf.add_chart_to_page(drawing, chart))
        idx += 1

    for sample in sample_data:
        drawing = Drawing(conf["width"], conf["height"], vAlign="TOP")
        sam = sample_data[sample]
        sam["sample"] = sample
        bars = bar_chart.get_bar_chart(conf, sam, "pdf")
        add_space()
        elements.append(pdf.add_chart_to_page(drawing, bars))
        idx += 1

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

    for sample in sample_data:
        conf["index"] = idx
        col_map = util.get_key_map(conf["line_charts"]["columns"], sample_data[sample])
        cn = round(sample_data[sample]["Full_length_CN_raw"]) / 2
        col_map["SMN2_CN_raw"] = [(x[0], (cn - (x[1] - cn))) for x in col_map["SMN1_CN_raw"]]
        chart = line_chart.get_line_chart(col_map, conf, sample, "svg")
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

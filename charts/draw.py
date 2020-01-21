import charts.histogram as histo
import charts.svg as svg
import charts.line_chart as line_chart
import charts.bar_chart as bar_chart
import charts.data_utils as util
from charts.svg_line_chart import sample_paths, circles


config = {
    "width": 800,
    "height": 200,
    "padding": 40,
    "pop_file": "/Users/awarren/Documents/Illumina/XiaoSMN/SMN_1kGP_results.tsv",
    "sample_file": "/Users/awarren/Documents/Illumina/XiaoSMN/SMN.json",
    "histograms": {
        "columns": ["Total_CN_raw", "Full_length_CN_raw"]
    },
    "line_charts": {
        "columns": ["SMN1_CN_raw"]
    },
    "bar_charts": {
        "columns": ["SMN1_read_support", "SMN2_read_support"]
    },
    "output_file": "/Users/awarren/Desktop/output.svg"
}


def get_height(conf, sample_count):
    histo_height = len(conf["histograms"]["columns"]) * (conf["height"] + conf["padding"])
    lines_height = len(conf["line_charts"]["columns"]) * (conf["height"] + conf["padding"])
    bars_height = sample_count * (conf["height"] + conf["padding"])
    return histo_height + lines_height + bars_height


def add_chart_to_page(page, chart):
    if page.value is None:
        page.value = [chart]
    else:
        page.value.append(chart)
    return page


def write_svg(conf):

    pop_data = util.read_pop_data(conf["pop_file"])
    sample_data = util.read_sample_data(conf["sample_file"])

    height = get_height(conf, len(sample_data.keys()))
    page = svg.headers(height)
    idx = 0
    for col in conf["histograms"]["columns"]:

        pop_col = util.get_pop_column(pop_data, col)
        sample_col_map = util.get_sample_col_map(sample_data, col)
        hist = histo.get_histogram(pop_col, sample_col_map, conf, col, idx)
        idx += 1
        page = add_chart_to_page(page, hist)

    for col in conf["line_charts"]["columns"]:
        sample_col_map = util.get_sample_col_map(sample_data, col)
        chart = line_chart.get_line_chart(sample_col_map, conf, col, idx)
        idx += 1
        page = add_chart_to_page(page, chart)

    for sample in sample_data:
        sam = sample_data[sample]
        sam["sample"] = sample
        bars = bar_chart.get_bar_chart(conf, sam, idx)
        idx += 1
        page = add_chart_to_page(page, bars)

    with open(config["output_file"], 'w') as fo:
        fo.write(page.to_string())


write_svg(config)



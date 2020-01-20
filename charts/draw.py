import charts.histogram as histo
import charts.svg as svg
import charts.line_chart as line_chart

config = {
    "width": 600,
    "height": 300,
    "padding": 40,
    "pop_file": "/Users/awarren/Documents/Illumina/XiaoSMN/SMN_1kGP_results.tsv",
    "sample_file": "/Users/awarren/Documents/Illumina/XiaoSMN/SMN.json",
    "histograms": {
        "columns": ["Total_CN_raw", "Full_length_CN_raw"],
        "width": 600,
        "height": 300,
        "padding": 40
    },
    "line_charts": {
        "columns": ["SMN1_CN_raw"],
        "width": 800,
        "height": 200,
        "padding": 40
    },
    "output_file": "/Users/awarren/Desktop/output.svg"
}


def get_height(conf):
    histo_height = len(conf["histograms"]["columns"]) * (conf["histograms"]["height"] + conf["histograms"]["padding"])
    lines_height = len(conf["line_charts"]["columns"]) * (conf["line_charts"]["height"] + conf["line_charts"]["padding"])
    return histo_height + lines_height


def write_svg(conf):
    height = get_height(conf)
    page = svg.headers(height)
    idx = 0
    for col in conf["histograms"]["columns"]:
        hist = histo.get_histogram(conf, col, idx)
        idx += 1
        if page.value is None:
            page.value = [hist]
        else:
            page.value.append(hist)

    for col in conf["line_charts"]["columns"]:
        chart = line_chart.get_line_chart(conf, col, idx)
        idx += 1
        if page.value is None:
            page.value = [chart]
        else:
            page.value.append(chart)

    with open(config["output_file"], 'w') as fo:
        fo.write(page.to_string())


write_svg(config)



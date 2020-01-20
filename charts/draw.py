import charts.histogram as histo

config = {
    "width": 600,
    "height": 300,
    "padding": 40,
    "pop_file": "/Users/awarren/Documents/Illumina/XiaoSMN/SMN_1kGP_results.tsv",
    "sample_file": "/Users/awarren/Documents/Illumina/XiaoSMN/SMN.tsv",
    "histograms": ["Total_CN_raw", "Full_length_CN_raw"],
    "output_file": "/Users/awarren/Desktop/output.svg"
}

histo.write_svg(config)


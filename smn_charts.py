import argparse
import charts.data_utils as util
from charts.draw import write_svg, write_pdf


def get_args():
    parser = argparse.ArgumentParser(description='Convenient pdf and svg charts for smn_caller output.')

    parser.add_argument('-p', '--pop-data',
                        dest="pop_data",
                        help='smn_caller.py output: Population tsv file',
                        required=True)

    parser.add_argument('-s', '--sample-data',
                        dest="sample_data",
                        help='smn_caller output: Sample JSON file',
                        required=True)

    parser.add_argument('-o', '--out-dir',
                        dest="out_dir",
                        help='Output directory',
                        required=True)

    args = parser.parse_args()
    return args


def main(conf):
    args = get_args()
    conf["pop_file"] = args.pop_data
    conf["sample_file"] = args.sample_data
    conf["output_dir"] = args.out_dir

    pop_data = util.read_pop_data(conf["pop_file"])
    sample_data = util.read_sample_data(conf["sample_file"])

    write_svg(conf, pop_data, sample_data)
    write_pdf(conf, pop_data, sample_data)


if __name__ == "__main__":
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
        "output_dir": "/Users/awarren/Desktop/"
    }
    main(config)

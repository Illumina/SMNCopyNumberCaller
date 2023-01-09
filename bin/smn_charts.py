import argparse
import SMNCopyNumberCaller.charts.data_utils as util
import os
from SMNCopyNumberCaller.charts.draw import write_svg, write_pdf

script_dir = os.path.abspath(os.path.dirname(__file__))


def get_args():
    parser = argparse.ArgumentParser(description='Convenient pdf and svg charts for smn_caller output.')

    parser.add_argument('-p', '--pop-data',
                        dest="pop_data",
                        help='smn_caller.py output: Population tsv file',
                        required=False)

    parser.add_argument('-s', '--sample-data',
                        dest="sample_data",
                        help='smn_caller output: Sample JSON file',
                        required=True)

    parser.add_argument('-o', '--out-dir',
                        dest="out_dir",
                        help='Output directory',
                        required=True)

    parser.add_argument('-v', '--svg',
                        dest="svg",
                        action='store_true',
                        help='Draw to svg instead of pdf',
                        required=False)

    args = parser.parse_args()
    return args


def main(conf):
    args = get_args()
    if args.pop_data is not None:
        conf["pop_file"] = args.pop_data
    conf["sample_file"] = args.sample_data
    conf["output_dir"] = args.out_dir

    pop_data = util.read_pop_data(conf["pop_file"])
    sample_data = util.read_sample_data(conf["sample_file"])

    if args.svg:
        write_svg(conf, pop_data, sample_data)
    else:
        write_pdf(conf, pop_data, sample_data)


if __name__ == "__main__":
    config = {
        "set_width": 800,
        "set_height": 200,
        "set_padding": 40,
        "width": 800,
        "height": 200,
        "padding": 40,
        "pop_file": os.path.join(script_dir, "charts/data/SMN_1kGP_results.tsv"),
        "sample_file": os.path.join(script_dir, "charts/data/example_smn.json"),
        "histograms": {
            "columns": ["Total_CN_raw", "Full_length_CN_raw"]
        },
        "line_charts": {
            "columns": ["SMN1_CN_raw"]
        },
        "bar_charts": {
            "columns": ["SMN1_read_support", "SMN2_read_support"]
        },
        "output_dir": script_dir
    }
    main(config)

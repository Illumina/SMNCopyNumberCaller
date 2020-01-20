import math
import charts.svg_histogram as svg_histo
import charts.svg as svg


def write_svg(config):

    page = svg.headers()

    for idx, col in enumerate(config["histograms"]):
        histo = get_histogram(config, idx)
        if page.value is None:
            page.value = [histo]
        else:
            page.value.append(histo)

    with open(config["output_file"], 'w') as fo:
        fo.write(page.to_string())


def get_histogram(config, idx=None):
    if idx is None:
        return
    else:
        col = config["histograms"][idx]

        pop_data = read_pop_data(config["pop_file"], col=col)
        sample_data = read_sample_data(config["sample_file"], col=col)

        x_axis = get_x_axis(pop_data, config["width"], config["padding"])
        y_axis = get_y_axis(pop_data, config["height"], config["padding"])

        histogram = svg_histo.get_svg(pop_data, sample_data, x_axis, y_axis, col=col)
        histogram.add_attr(["x", "0"])
        histogram.add_attr(["y", "%s" % (idx * (config["height"] + config["padding"]))])

        return histogram


def add_to_map(data_map, key):
    if key in data_map:
        data_map[key] += 1
    elif key not in data_map:
        data_map[key] = 1

    return data_map


def read_pop_data(data_file, col="Total_CN_raw"):
    data_map = {}

    with open(data_file) as fi:
        first = True

        for line in fi:
            spl = line.split('\t')
            idx = 6

            if first:
                first = False
                for i, column in enumerate(spl):
                    if column == col:
                        idx = i
            else:
                cn = round(float(spl[idx]), 2)
                data_map = add_to_map(data_map, cn)

    return data_map


def read_sample_data(sample_file, col):
    sample_map = {}
    first = True

    with open(sample_file, 'r') as fi:

        for line in fi:
            spl = line.split('\t')
            idx = 6

            if first:
                first = False
                for i, column in enumerate(spl):
                    if column == col:
                        idx = i

            else:
                sample = spl[0]
                cn = round(float(spl[idx]), 2)
                sample_map[sample] = cn

    return sample_map


def get_x_axis(pop_data, width, padding):
    minimum = math.floor(min(pop_data.keys()))
    maximum = round(max(pop_data.keys()))

    return {
        "min": minimum,
        "max": maximum,
        "tics": range(minimum, maximum),
        "title": "Copy Number",
        "domain": [padding, width - padding]
    }


def get_y_axis(pop_data, height, padding):
    minimum = 0
    maximum = round(max(pop_data.values()))

    return {
        "min": minimum,
        "max": maximum,
        "tics": range(minimum, maximum, 20),
        "title": "Sample Count",
        "domain": [padding, height - padding]
    }

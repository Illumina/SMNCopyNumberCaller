import json


def add_to_map(data_map, key):
    if key in data_map:
        data_map[key] += 1
    elif key not in data_map:
        data_map[key] = 1

    return data_map


def get_json(line, headers):
    sample_data = {}
    for i, val in enumerate(line):
        sample_data[headers[i]] = val
    return sample_data


def read_pop_data(data_file):
    data = []
    headers = []

    with open(data_file) as fi:
        first = True

        for line in fi:
            spl = line.rstrip('\n').split('\t')

            if first:
                first = False
                headers = spl

            else:
                data.append(get_json(spl, headers))

    return data


def read_sample_data(data_file):
    allowed_sites = [6, 7, 9, 10, 11, 12, 13, 14]
    relevant_fields = ["SMN1_read_support", "SMN2_read_support", "SMN1_fraction", "SMN1_CN_raw", "Confidence"]

    with open(data_file, 'r') as fi:
        data = json.load(fi)

        for sample in data:
            for field in relevant_fields:
                arr = data[sample][field]
                data[sample][field] = [(i + 1, x) for i, x in enumerate(arr) if i in allowed_sites]

        return data


def get_pop_column(pop_data, column):
    data_map = {}
    for line in pop_data:
        cn = round(float(line[column]), 2)
        data_map = add_to_map(data_map, cn)
    return data_map


def get_sample_col_map(sample_data, column):
    result = {}
    for sample in sample_data:
        result[sample] = sample_data[sample][column]

    return result


def get_key_map(cols, data):
    col_map = {}
    for col in cols:
        col_map[col] = data[col]

    return col_map

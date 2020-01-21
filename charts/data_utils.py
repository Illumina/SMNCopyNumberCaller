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
    with open(data_file, 'r') as fi:
        return json.load(fi)


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

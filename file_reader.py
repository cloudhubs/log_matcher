import json
import os
import itertools
from json import JSONDecodeError


def read_json_file(path):
    result_list = []

    if not os.path.exists(path) or not os.path.isfile(path):
        err = Exception("Could not open file")
        raise err

    with open(path, encoding='utf-8') as f:
        result_list = json.load(f)

    return result_list


if __name__ == "__main__":
    results = read_json_file("./test_data_aggregator.txt")

    print(results)

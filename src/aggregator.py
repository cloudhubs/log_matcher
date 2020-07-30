from src import file_reader
import json

# Definition: convert intermediary data to output step
# @params: data a JSON formatted piece of data from an intermediary file type
# @return: a string with the calculated output data in JSON form
def aggregate_data(data):
    output_data = []

    for sig in data.keys():
        dict = {sig: {}}

        # data points
        dict[sig]["Unique Values"] = len(data[sig].keys())
        dict[sig]["Unique Matches"] = 0
        dict[sig]["Total Matches"] = 0
        dict[sig]["Total Values"] = 0

        for value in data[sig].keys():
            if data[sig][value][0] > 0:
                dict[sig]["Unique Matches"] += 1
            dict[sig]["Total Matches"] += data[sig][value][0]
            dict[sig]["Total Values"] += data[sig][value][1]

        output_data.append(dict)

    return output_data

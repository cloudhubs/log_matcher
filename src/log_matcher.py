from src import file_reader
import json


# Name: match_logs
# Input: 2 log files in JSON format after extracting the singatures
#        examples are test_data/test_data_aggregator.txt and test_data/test_data_pipeline.txt
# Output: Form data on each regex and individual field on number of matches and occurrences of data
#          example is test_data/test_data/intermediary.txt
# Definition: convert input data to intermediary step
def match_logs(logs_a, logs_b):
    match_data_a = get_log_data(logs_a)
    match_data_b = get_log_data(logs_b)
    regex_a = get_key_regex(logs_a)
    regex_b = get_key_regex(logs_b)

    # go through each log file, adding to the aggregate and incrementing matches
    match_data_aggregate = {}
    for a_keys in list(regex_a.keys()):
        for b_keys in list(regex_b.keys()):
            # check if they share any regex
            if not set(regex_a[a_keys]).isdisjoint(regex_b[b_keys]):
                match_string = a_keys + "," + b_keys
                match_data_aggregate[match_string] = {}
                value_tracker = []  # keeps track of the values added
                # add values from a
                for value in list(match_data_a[a_keys].keys()):
                    match_data_aggregate[match_string].update({value: match_data_a[a_keys][value]})
                    value_tracker.append(value)

                # add values from b, matching if possible
                for value in list(match_data_b[b_keys].keys()):
                    # check if there's a match
                    if value in value_tracker:
                        # match
                        match_data_aggregate[match_string][value][0] = match_data_aggregate[match_string][value][1] * \
                                                                       match_data_b[b_keys][value][1]
                        match_data_aggregate[match_string][value][1] += match_data_b[b_keys][value][1]
                    else:
                        match_data_aggregate[match_string].update({value: match_data_b[b_keys][value]})

    return match_data_aggregate


# Name: get_log_data
# Input: log_file: in JSON format after gathering all REGEX and variable features
#        example of input in test_data/test_data_aggregator.txt
# Output: For each unique regex, the values and number of matches and occurrences
#         The number of matches will be 0 at this time, as no matching has occurred.
# Definition: Convert the signatures of a log file to an aggregate form of all the
#             seen, individual variables, group them by their regular expression, and
#             list their occurrences, as well as available opening for matches
def get_log_data(log_file):
    log_data = {}
    # go through first log file, aggregating the data on the regex
    for log_type in log_file.keys():
        for key_name in list(log_file[log_type].keys()):
            if key_name not in log_data:
                log_data[key_name] = {}
            for regex in log_file[log_type][key_name]:
                for item in log_file[log_type][key_name][regex]:
                    value = list(item.keys())[0]
                    lines_of_code = len(item[value])

                    # check if value already exists in key domain
                    if value in log_data[key_name]:
                        # update line count
                        log_data[key_name][value][1] += lines_of_code
                    else:
                        # add log entry
                        log_data[key_name][value] = [0, lines_of_code]

    return log_data


# returns the mapping of keys to their possible regex representations
def get_key_regex(log_file):
    key_data = {}

    for log_type in log_file.keys():
        for key_id in list(log_file[log_type].keys()):
            if key_id not in key_data:
                # new key name
                key_data[key_id] = []
            key_data[key_id].extend((log_file[log_type][key_id].keys()))

    return key_data


if __name__ == "__main__":
    data = match_logs(file_reader.read_json_file("../test_data/test_data_aggregator.txt"),
                      file_reader.read_json_file("../test_data/test_data_pipeline.txt"))
    with open('sample_out.txt', 'w') as f:
        json.dump(data,f)
    print(data)

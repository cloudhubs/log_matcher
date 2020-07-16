from src import file_reader


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
            if not a_keys.disjoint(b_keys):
                match_string = a_keys + "," + b_keys
                match_data_aggregate[match_string] = {}
                value_tracker = []  # keeps track of the values added
                # add values from a
                for entry in match_data_a[a_keys]:
                    match_data_aggregate[match_string].update(entry)
                    value_tracker.append(list(entry.keys())[0])

                # add values from b, matching if possible
                for entry in match_data_b[b_keys]:
                    # check if there's a match
                    value = list(entry.keys())[0]
                    if value in value_tracker:
                        # match
                        match_data_aggregate[match_string][value][0] = match_data_aggregate[match_string][value][1] * \
                                                                       entry[1]
                        match_data_aggregate[match_string][value][1] += entry[1]
                    else:
                        match_data_aggregate[match_string].update(entry)

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
    match_data = {}
    # go through first log file, aggregating the data on the regex
    for log_type in log_file.keys():
        key_index = 0
        key_names = log_type.split(",")
        for item in log_file[log_type]:
            for regex in item.keys():
                if key_names[key_index] not in match_data.keys():
                    match_data[key_names[key_index]] = {}
                # get each individual value of each regex
                for entry in item[regex]:
                    key = list(entry.keys())[0]
                    lines_of_code = list(entry.values())[0]
                    # check if this is a duplicate value, or new
                    if key not in match_data[key_names[key_index]]:
                        match_data[key_names[key_index]][key][0] = [0, len(lines_of_code)]
                    else:
                        match_data[key_names[key_index]][key][1] += len(lines_of_code)
        key_index += 1

    return match_data

# returns the 
def get_key_regex(log_file):
    key_data = {}

    for log_type in log_file.keys():
        key_index = 0
        key_names = log_type.split(",")
        for item in log_file[log_type]:
            if key_names[key_index] not in key_data:
                key_data[key_names[key_index]] = []
            # add the mapping of the regex to the key
            key_data[key_names[key_index]].append(list(log_file[log_type][item].keys())[0])
            key_index += 1

    print(key_data)
    return key_data


if __name__ == "__main__":
    data = match_logs(file_reader.read_json_file("../test_data/test_data_aggregator.txt"),
                      file_reader.read_json_file("../test_data/test_data_pipeline.txt"))
    print(data)

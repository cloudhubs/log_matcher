from src import file_reader


# Definition: convert input data to intermediary step
def match_logs(logs_a, logs_b):
    match_data_a = {}
    match_data_b = {}
    match_data_aggregate = {}

    match_data_a = get_log_data(logs_a)
    match_data_b = get_log_data(logs_b)

    return 0


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
        for regex in log_file[log_type].keys():
            if regex not in match_data.keys():
                match_data[regex] = {}
            # get each individual value of each regex
            for entry in log_file[log_type][regex]:
                key = list(entry.keys())[0]
                lines_of_code = list(entry.values())[0]
                # check if this is a duplicate value, or new
                if key not in match_data[regex]:
                    match_data[regex][key] = [0, len(lines_of_code)]
                else:
                    match_data[regex][key][1] += len(lines_of_code)

    return match_data


if __name__ == "__main__":
    match_logs(file_reader.read_json_file("../test_data/test_data_aggregator.txt"),
               file_reader.read_json_file("../test_data/test_data_pipeline.txt"))

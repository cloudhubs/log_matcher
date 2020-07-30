from src import match_selector, input_generator, aggregator, log_matcher


# Name: Cluster Log Files Raw
# Output: The primary candidate for log clustering
# Input: files to pipeline and aggregator logs (raw)
# Description: takes a pipeline and aggregator log file and finds the primary candidate for clustering
def cluster_log_files_raw(path_a, path_b):
    # generate input
    log_data_a = input_generator.generate_big_obj(path_a)
    log_data_b = input_generator.generate_big_obj(path_b)

    return cluster_log_files(log_data_a, log_data_b)


# Name: Cluster Log Files Raw
# Output: The primary candidate for log clustering
# Input: files to pipeline and aggregator logs in expected JSON format following simple log clustering and
#        signature extraction
# Description: takes a pipeline and aggregator log file and finds the primary candidate for clustering
def cluster_log_files(log_data_a, log_data_b):
    # get defined versions of the data
    agg_a = aggregator.aggregate_data(log_data_a)
    agg_b = aggregator.aggregate_data(log_data_b)

    # match the data
    matches = log_matcher.match_logs(agg_a, agg_b)

    # find primary candidate
    return match_selector.get_primary_match(matches)

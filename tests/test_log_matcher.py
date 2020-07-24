import pytest, _pytest
from src import file_reader, log_matcher


def test_match_logs():
    input_pipeline = file_reader.read_json_file("../test_data/test_data_pipeline.txt")
    input_agg = file_reader.read_json_file("../test_data/test_data_aggregator.txt")
    output = file_reader.read_json_file("../test_data/test_data_matching.txt")

    match_data = log_matcher.match_logs(input_pipeline, input_agg)

    assert match_data == output

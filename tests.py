import pytest
import file_reader
import aggregator


# stub
def test_aggregate_logs():
    input_pipeline = file_reader.read_json_file("./test_data/test_data_pipeline.txt")
    input_agg = file_reader.read_json_file("./test_data/test_data_aggregator.txt")
    output = file_reader.read_json_file("./test_data/test_data_intermediary.txt")

    aggregation = aggregator.aggregate_logs(input_pipeline, input_agg)

    assert aggregation == output


def test_aggregate_data():
    input = file_reader.read_json_file("./test_data/test_data_intermediary.txt")
    output = file_reader.read_json_file("./test_data/test_data_output.txt")

    data = aggregator.aggregate_data(input)

    assert data == output
from src import aggregator, file_reader


def test_aggregate_data():
    input = file_reader.read_json_file("../test_data/test_data_matching.txt")
    output = file_reader.read_json_file("../test_data/test_data_output.txt")

    data = aggregator.aggregate_data(input)

    assert data == output

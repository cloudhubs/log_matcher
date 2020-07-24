from src import file_reader

MATCH_WEIGHT = 1.0
VALUE_WEIGHT = 1.0
GLOBAL_WEIGHT = 1.0


class Match:
    def __init__(self, name, unique_matches, total_matches, unique_values, total_values):
        self.name = name
        self.unique_matches = unique_matches
        self.total_matches = total_matches
        self.unique_values = unique_values
        self.total_values = total_values


def score(match, global_value_count):
    match_score = 1

    # score by unique_match/total_match ratio (higher = better)
    match_score *= (match.unique_matches / match.total_matches) * MATCH_WEIGHT

    # score by unique_value/total_value ratio (higher = better)
    match_score *= (match.unique_values / match.total_values) * VALUE_WEIGHT

    # score by total_value/global_value ratio (higher = better)
    match_score *= (match.total_values / global_value_count) * GLOBAL_WEIGHT

    return match_score


def get_primary_match(match_output):
    match_objects = []
    global_value_count = 0

    # turn results into match objects
    for result in match_output:
        name = list(result.keys())[0]
        unique_matches = result[name]["Unique Matches"]
        total_matches = result[name]["Total Matches"]
        unique_values = result[name]["Unique Values"]
        total_values = result[name]["Total Values"]
        global_value_count += total_values

        match = Match(name, unique_matches, total_matches, unique_values, total_values)
        match_objects.append(match)

    # assign scores
    for match in match_objects:
        match.score = score(match, global_value_count)

    # get best score
    match_objects.sort(key=lambda s: s.score, reverse=True)
    return match_objects[0].name


if __name__ == "__main__":
    print(get_primary_match(file_reader.read_json_file("../test_data/test_data_output.txt")))

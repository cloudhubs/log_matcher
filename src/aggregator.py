import file_reader


# Definition: Class which holds all the attributes of an output JSON line
class Output:
    signature = ""
    unique_matches = 0
    matches = 0
    unique_values = 0
    total_values = 0

    # Definition: Converts the obejct to a String format for output to a file or to stdout
    # @params: self the "this" object to print
    # @return: a string with all the attributes printed in JSON format
    def __str__(self):
        return "\t{\"" + self.signature + "\": [" + str(self.unique_matches) + "," + str(self.matches) + "," + str(
            self.unique_values) + "," + str(self.total_values) + "]},\n"


# Definition: convert intermediary data to output step
# @params: data a JSON formatted piece of data from an intermediary file type
# @return: a string with the calculated output data in JSON form
def aggregate_data(data):
    output_data = []

    for sig in data.keys():
        obj = Output()
        obj.signature = sig
        obj.unique_values = len(data[sig].keys())

        for value in data[sig].keys():
            if data[sig][value][0] > 0:
                obj.unique_matches += 1
            obj.matches += data[sig][value][0]
            obj.total_values += data[sig][value][1]

        output_data.append(obj)

    output_string = "[\n"
    for obj in output_data:
        output_string += str(obj)
    output_string += "]"

    return output_string


if __name__ == "__main__":
    print(aggregate_data(file_reader.read_json_file("../test_data/test_data_matching.txt")))

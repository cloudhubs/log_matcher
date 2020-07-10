import file_reader

class Output:
    signature=""
    unique_matches=0
    matches=0
    unique_values=0
    total_values=0

    def __str__(self):
        return "\t{\"" + self.signature + "\": [" + str(self.unique_matches) + "," + str(self.matches) + "," + str(self.unique_values) + "," + str(self.total_values) + "]},\n"

# Definition: convert intermediary data to output step
def aggregate_data(data):
    output_data=[]

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

data = aggregate_data(file_reader.read_json_file("../test_data/test_data_intermediary.txt"))
print(data)
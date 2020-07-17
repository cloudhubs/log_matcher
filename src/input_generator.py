import re
import json

class BigObj:
    line_type = []
    regex_items = []


class Regex:
    regex = ""
    values = []
    line_numbers = []

# Verify if a line is in JSON format
# @params myjson: the object to verify json form of
# @return boolean indicating whether the object can be parsed into json
def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True

# Extracts lines from log file in json format
# @params pipeline_path: the file to extract the logs from
# @return array of all the logs as json objects
def get_log_list(file_path):
    log_list = []

    file = open(file_path)
    # Determine if only the first line of the file was not json
    for line in file:
        log_list.append(json.loads(line))

    return log_list

# @description iterates through all of the logs, generating regex strings for all the values
# @param file_path: a file_path to the log items in JSON form
# @return a list of BigObj's completely implemented
def generate_big_obj(file_path):
    objects = []  # list of big objects
    log_items = get_log_list(file_path)
    lines = []  #
    line_types = []

    for i in range(0, len(log_items)):
        # get the line types and the values that were used to get the regex
        line_type = get_line_type(log_items[i])[0]
        line_values = get_line_type(log_items[i])[1]

        # if the line type already exists, find it in the line_types
        if line_type in line_types:
            for g in range(0, len(objects)):
                if line_type == objects[g].line_type:
                    regex_items = objects[g].regex_items
                    # iterate through the regex items to find if the value is new or already found
                    for p in range(0, len(regex_items)):
                        if isinstance(line_values[p], list):
                            for q in range(len(line_values[p])):
                                # if the value has already been found, add the line number
                                if line_values[p][q] in regex_items[p].values:
                                    for v in range(0, len(regex_items[p].values)):
                                        if regex_items[p].values[v] == line_values[p][q]:
                                            regex_items[p].line_numbers[v].append(i)
                                else:
                                    regex_items[p].values.append(line_values[p][q])
                                    regex_items[p].line_numbers.append([i])
                        else:
                            # if the value has already been found, add the line number
                            if line_values[p] in regex_items[p].values:
                                for v in range(0, len(regex_items[p].values)):
                                    if regex_items[p].values[v] == line_values[p]:
                                        regex_items[p].line_numbers[v].append(i)
                            # if the value is new, add the value and a new list for its line numbers
                            else:
                                regex_items[p].values.append(line_values[p])
                                regex_items[p].line_numbers.append([i])

        # new line type
        else:
            line_types.append(line_type)
            item = BigObj()
            item.line_type = line_type
            item.regex_items = []

            # iterate through each regex type
            for h in range(0, len(item.line_type)):
                item.regex_items.append(Regex())
                if isinstance(item.regex_items[h].values, list):
                    for v in line_values:
                        item.regex_items[h].values.append(v)
                        item.regex_items[h].line_numbers.append([i])
                else:
                    # add a Regex object with a regex, list of values, and list of line numbers for each value
                    item.regex_items[h].values = [line_values[h]]
                    item.regex_items[h].line_numbers = [[i]]

                item.regex_items[h].regex = item.line_type[h]

            objects.append(item)

            #print(item.line_type)
            #for reg in item.regex_items:
            #    print("\t" + reg.regex)
            #    for k in range(0, len(reg.values)):
            #        print("\t\t", reg.values[k], reg.line_numbers[k])
    return objects

# @description generates a list of all the different regex values in a line
# @param log_item: a dict type object to generate the regex strings for while ignoring time, message, and -1 values
# @return a list of the regex values in order
def get_line_type(log_item):
    # array of all the line types present in this log line
    line_type = []
    line_values = []
    # iterate through each log item key
    for item, value in log_item.items():
        if "time" not in item and "message" not in item and "-1" not in str(value):
            reg = get_regex(str(value))
            if len(reg) > 0:
                line_type.append(reg)
                line_values.append(value)
    return line_type, line_values


# @description creates a regex string for digits or strings with special characters
# @param value: the string to create the regex for
# @return the regex string for the given value
def get_regex(value):
    line = ""
    # create a regex for a number
    if value.isdigit():
        for i in range(0, len(value)):
            line += "\d"
    # create a regex for a string
    else:
        if isinstance(value, list):
            for i in range(0, len(value[0])):
                if re.match("[a-zA-z0-9]", value[0][i]):
                    line += "[a-zA-z0-9]"
                else:
                    if value[0] != '\"' and value[0] != "{" and value[0] != "}":
                        line += ("[" + value[0][i] + "]")
        else:
            for i in range(0, len(value)):
                if re.match("[a-zA-z0-9]", value[i]):
                    line += "[a-zA-z0-9]"
                else:
                    if value != '\"' and value != "{" and value != "}":
                        line += ("[" + value[i] + "]")
    return line


obj = generate_big_obj("../test_data/pipelineout.txt")
f = open("testOutput.txt", "w")
for item in obj:
    f.write("\t")
    for type in item.line_type:
        f.write(type)
    f.write("\n")
    for reg in item.regex_items:
        f.write("\t" + reg.regex)
        for k in range(0, len(reg.values)):
            f.write("\t\t")
            f.write(str(reg.values[k]))
            for num in reg.line_numbers[k]:
                f.write(str(num) + ", ")
            f.write("\n")

f.close()
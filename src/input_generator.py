import re
import json


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
    big_dictionary = {}
    log_items = get_log_list(file_path)
    for i in range(0, len(log_items)):
        # get the string line type
        line_type = get_line_type(log_items[i])[0]
        line_values = get_line_type(log_items[i])[1]
        regex = get_line_type(log_items[i])[2]

        str_line_type = ""
        for type in line_type:
            str_line_type += type + ","
        str_line_type = str_line_type[0:len(str_line_type) - 1]

        # add the values and line numbers to the regex if the line-type has been found
        if str_line_type in big_dictionary:
            for j in range(0, len(regex)):
                if regex[j] not in big_dictionary[str_line_type][line_type[j]]:
                    big_dictionary[str_line_type][line_type[j]][regex[j]] = []
                    big_dictionary[str_line_type][line_type[j]][regex[j]].append({line_values[j]: [i]})
                else:
                    found = False
                    for k in range(len(big_dictionary[str_line_type][line_type[j]][regex[j]])):
                        if line_values[j] in big_dictionary[str_line_type][line_type[j]][regex[j]][k]:
                            found = True
                            big_dictionary[str_line_type][line_type[j]][regex[j]][k][line_values[j]].append(i)
                    # if line_values[j] in big_dictionary[str_line_type][line_type[j]][regex[j]]:
                    #    big_dictionary[str_line_type][line_type[j]][regex[j]][line_values[j]].append(i)
                    # else:
                    #    big_dictionary[str_line_type][line_type[j]][regex[j]][line_values[j]] = [i]
                    if not found:
                        big_dictionary[str_line_type][line_type[j]][regex[j]].append({line_values[j]: [i]})
        # create the regex dictionaries
        else:
            big_dictionary[str_line_type] = {}
            for j in range(0, len(regex)):
                big_dictionary[str_line_type][line_type[j]] = {}
                # big_dictionary[str_line_type][line_type[j]][regex[j]] = {}
                # big_dictionary[str_line_type][line_type[j]][regex[j]][line_values[j]] = [i]
                big_dictionary[str_line_type][line_type[j]][regex[j]] = []
                big_dictionary[str_line_type][line_type[j]][regex[j]].append({line_values[j]: [i]})

    return big_dictionary


# @description generates a list of all the different regex values in a line
# @param log_item: a dict type object to generate the regex strings for while ignoring time, message, and -1 values
# @return a list of the regex values in order
def get_line_type(log_item):
    # array of all the line types present in this log line
    line_type = []
    regex_vals = []
    line_values = []
    # iterate through each log item key
    for item, value in log_item.items():
        if "time" not in item and "message" not in item and "warning" not in item and "error" not in item and value != -1:
            reg = get_regex(str(value))
            if len(reg) > 0:
                regex_vals.append(reg)
                line_type.append(item)
                line_values.append(value)
    return line_type, line_values, regex_vals


# @description creates a regex string for digits or strings with special characters
# @param value: the string to create the regex for
# @return the regex string for the given value
def get_regex(value):
    line = ""
    count = 0
    # create a regex for a number
    if value.isdigit():
        line += (str(len(value)) + "d")
    # create a regex for a string
    else:
        for i in range(0, len(value)):
            if re.match("[a-zA-z0-9]", value[i]):
                count += 1

            elif value != '\"' and value != "{" and value != "}":
                if count > 0:
                    line += (str(count) + "c")
                    count = 0
                line += value[i]
    if count > 0:
        line += (str(count) + "c")
    return line

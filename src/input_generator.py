import re

class BigObj:
    line_type=""
    regex_items=[]

class Regex:
    regex=""
    line_items=[]

class Line:
    value=""
    line_numbers=[]


def generate_big_obj(file_path):
    objects=[]
    log_items = get_log_list(file_path)
    line_types = []
    lines = []

    for i in range(0, len(log_items)):
        item = BigObj()
        line_type = get_line_type(log_items[i])
        if line_types.__contains__(self, line_type):
            for j in range(len(line_types)):
                if line_type == line_types[j]:
                    lines[j].append(i)

    return objects


def get_log_list(file_path):
    log_list = [{}]

    # Determine if only the first line of the file was not json
    for line in open(file_path, encoding='utf-8'):
        if is_json(line):
            log_list.append(json.loads(line))

    return log_list


def get_line_type(log_item):
    # array of all the line types present in this file
    line_type = []

    # iterate through each log item key
    for key in log_item.keys(self):
        # create a regex for a number
        if log_item[key].isdigit():
            line_type.append(str(len(log_item[key])) + "d")
        # create a regex for a string
        #else:
            # iterate through each character and check if the character is a letter/number
            # if it's a special character, that will be added to the regex

thing = re.compile('1000')
print(thing)
#print(generate_big_obj("test_data/pipelineout.txt"))
from os.path import abspath, join, dirname

MAIN_PATH = dirname(__file__)
LOGS_PATH = join(MAIN_PATH, 'Logs')

LOGS = ['Rhudney - 27_10.txt']
DATA_LABELS = ['RPM', 'SPEED', 'THROTTLE']

log_paths = []

def set_log_full_path(log_paths):
    new_log_paths = []
    for path in log_paths:
        new_path = join(LOGS_PATH, path)
        new_log_paths.append(new_path)
    return new_log_paths

def read_file_by_path(path):
    with open(path, 'r') as log:
        content = log.readlines()
    return content

def new_log_dict():
    new_dict = {}
    for label in DATA_LABELS:
        new_dict[label] = []
    return new_dict

def process_line(line):
    # Must separate the line among KEY and VALUE.
    new_line = line.replace(' ', '').replace('\n', '').split(':')
    key = new_line[0]
    value = new_line[1]

    return key, value

def is_valid_line(line):
    new_line = line.replace(' ', '').replace(r'\n', '').split(':')

    if len(new_line) < 2:
        return False
    elif (new_line[0] in DATA_LABELS):
        return True
    else:
        return False

def execute_each_log(log_paths):
    for log_path in log_paths:
        content = read_file_by_path(log_path)

        # Creates a dict of lists of values.
        data_dict = new_log_dict()

        # Processes line by line.
        for line in content:

            if is_valid_line(line=line):
                key, value = process_line(line=line)
                data_dict[key].append(value)


log_paths = set_log_full_path(log_paths = LOGS)
execute_each_log(log_paths = log_paths)



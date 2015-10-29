from os.path import abspath, join, dirname

MAIN_PATH = dirname(__file__)
LOGS_PATH = join(MAIN_PATH, 'Logs')

LOGS = ['Rhudney - 27_10.txt']
DATA_LABELS = ['RPM', 'SPEED', 'THROTTLE']

PERIOD = 0.300 #miliseconds

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

def normalize_dict_lists(data_dict):
    min_lists_lenght = min([len(value) for key, value in data_dict.items()])

    for key, value in data_dict.items():
        data_dict[key] = value[:min_lists_lenght]

    return data_dict

def execute_each_log(log_paths):
    log_dicts = []
    for log_path in log_paths:
        content = read_file_by_path(log_path)

        # Creates a dict of lists of values.
        data_dict = new_log_dict()

        # Processes line by line.
        for line in content:

            if is_valid_line(line=line):
                key, value = process_line(line=line)
                data_dict[key].append(value)

        data_dict = normalize_dict_lists(data_dict=data_dict)
        log_dicts.append(data_dict)

    return log_dicts

def post_process_dicts(log_dicts):
    return log_dicts
    # Create the list of Acceleration and include it to the dict.

# According to period and the list_length this function creates a list with:
# - Same length of list_lenght.
# - Each of its values is equal to: period*element_index_in_the_list
def build_x_axis_values(period, list_lenght):
    x_axis = [round(idx*period, 1) for idx in range(list_lenght)]
    return x_axis

def plot_graphs(log_dicts, x_axis):
    import matplotlib.pyplot as plt

    # LABELS QTT.
    numrows = len(DATA_LABELS)
    NUMCOLUMS = 1

    for idx, log in enumerate(log_dicts):
        # Choose a 'name' for the figure. idx is the name.
        fig_number = idx+1
        plt.figure(fig_number)
        for idx_label, label in enumerate(DATA_LABELS):
            label_figure = idx_label + 1

            # subplot(numrows, numcols, fignum)
            plt.subplot(numrows, NUMCOLUMS, label_figure)
            plt.plot(x_axis, log[label])
            plt.ylabel(label)

    plt.show()

log_paths = set_log_full_path(log_paths = LOGS)
# Dicionario de cada Log de dados.
# KEYS = ['RPM','THROTTLE','SPEED']
log_dicts = execute_each_log(log_paths = log_paths)

# POST-PROCESS DICTS
log_dicts = post_process_dicts(log_dicts = log_dicts)

# CREATES THE X_AXIS LIST
list_length = len(log_dicts[0]['SPEED'])
x_axis = build_x_axis_values(PERIOD, list_length)

# PLOT GRAPHS
plot_graphs(log_dicts = log_dicts, x_axis = x_axis)



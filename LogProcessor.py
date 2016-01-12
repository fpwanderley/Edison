# -*- coding: utf-8 -*-
from os.path import join, dirname
from UseCases import StrongBreakCase, CorrectGearChangingCase
import time
from SenderClass import Sender
from ChartProcessors import build_x_axis_values, plot_graphs

MAIN_PATH = dirname(__file__)
LOGS_PATH = join(MAIN_PATH, 'Logs')

LOGS = ['Rhudney - 27_10.txt']
DATA_LABELS = ['RPM', 'SPEED', 'THROTTLE']

PERIOD = 0.600 #miliseconds

START_COMMAND = 'start'
FINISH_COMMAND = 'finish'

SHOULD_PLOT = False
SHOULD_SEND = True

def timestamp(idx, period):
    """ Formata idx e period em segundos para ser utilizado como timestamp

    :param idx: indice de um for loop.
    :param period: period em segundos
    :return: Timestamp formatado.
    """

    total_seconds = idx*period

    int_seconds = int(total_seconds)
    cent_seconds = int((total_seconds - int_seconds)*100)

    return ('{0}.{1}').format(int_seconds, cent_seconds)

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

def post_process_dicts(log_dicts):
    """ Processa e cria novos dicts.

    1: Cria o dict com os THROTTLES normalizados.

    2: Cria o dict com ACCELERATION baseado em SPEED.

    :param log_dicts: Os dicts existents atualmente
    :return: Os dicts atuais com os novos.
    """

    for dict in log_dicts:

        # Normalizing Throttle
        old_dict = dict.pop('THROTTLE')
        dict['THROTTLE'] = normalize_throttle(old_dict)

        # Finding Acceleration
        speed_list = dict['SPEED']
        dict['ACCELERATION'] = create_derivative(speed_list, period = PERIOD)
        DATA_LABELS.append('ACCELERATION')

        # Finding RPM derivative.
        rpm_list = dict['RPM']
        dict['RPM_DERIVATIVE'] = create_derivative(rpm_list, period = PERIOD)
        DATA_LABELS.append('RPM_DERIVATIVE')

    return log_dicts

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

    # POST-PROCESS DICTS
    log_dicts = post_process_dicts(log_dicts = log_dicts)

    return log_dicts

def normalize_throttle(throttle_list):

    int_list = [int(x) for x in throttle_list]

    max_int = max(int_list)
    min_int = min(int_list)

    def normalizer(element):
        return (element - min_int)*100/(max_int - min_int)

    return [str(normalizer(x)) for x in int_list]

def create_derivative(value_list, period):
    """ Calcula as derivadas de uma lista de valores.

    :param value_list: Lista de valores.
    :param period: O período para o cálculo da derivada.
    :return: Uma lista com as derivadas da entrada.
    """

    acceleration_list = []
    int_speed_list = [int(x) for x in value_list]
    last_speed = int_speed_list[0]

    for speed in int_speed_list:

        acceleration = round((speed - last_speed)/period, 2)
        acceleration_list.append(acceleration)
        last_speed = speed

    str_acceleration_list = [str(x) for x in acceleration_list]
    return str_acceleration_list

log_paths = []

# Sets the full path for all Logs.
log_paths = set_log_full_path(log_paths = LOGS)

# Returns a list of Dicts. A Dict for each log with the entries:
# 'RPM', 'SPEED', 'THROTTLE', 'ACCELERATION', 'RPM_DERIVATIVE'
log_dicts = execute_each_log(log_paths = log_paths)

# PLOT ALL GRAPHS: Only for analysis.
if SHOULD_PLOT:
    list_length = len(log_dicts[0]['SPEED'])
    x_axis = build_x_axis_values(PERIOD, list_length)
    plot_graphs(log_dicts = log_dicts, x_axis = x_axis)

# For each log_dict there is only one process between Edison and Server.
for dict in log_dicts:

    analysis_lenght = len(dict['RPM'])

    # Initializing the UseCases
    strong_break_case = StrongBreakCase(period = PERIOD)
    changing_gear_case = CorrectGearChangingCase(period = PERIOD)

    # Initializing the Communication class
    if SHOULD_SEND:
        sender = Sender()
        sender.start_process(START_COMMAND)

    # Runs through every dict entry and feeds the respective Case.
    for idx in range(analysis_lenght):

        #################################
        ### Feed the analysis classes ###
        #################################
        # StrongBreakCase:
        current_acceleration = dict['ACCELERATION'][idx]
        strong_break_case.include_new_entry(new_entry = current_acceleration)

        # CorrectGearChangingCase:
        current_acceleration_derivative = float(dict['RPM_DERIVATIVE'][idx])
        current_rpm = int(dict['RPM'][idx])
        current_speed = int(dict['SPEED'][idx])
        changing_gear_case.include_new_entry(rpm_derivative = current_acceleration_derivative,
                                             rpm = current_rpm,
                                             speed = current_speed)

        #########################################
        ### Get message from analysis classes ###
        #########################################
        # StrongBreakCase:
        strong_break_case_message = strong_break_case.get_current_message(idx = idx)

        # CorrectGearChangingCase:
        changing_gear_case_message = changing_gear_case.get_current_message()

        #########################################
        ### Send the message to the server    ###
        #########################################
        if SHOULD_SEND:
            timestamp_str = ('{0}').format(timestamp(idx=idx, period=PERIOD))
            if strong_break_case_message is not None:
                message = ('BreakCase: {0}').format(strong_break_case_message)
                sender.send_message(message=strong_break_case_message,
                                    timestamp=timestamp_str,
                                    case='break')
            if changing_gear_case_message is not None:
                sender.send_message(message=changing_gear_case_message,
                                    timestamp=timestamp_str,
                                    case='gear')
        # Else it prints
        else:
            print ('{0}').format(timestamp(idx=idx, period=PERIOD))
            if strong_break_case_message:
                print ('BreakCase: {0}').format(strong_break_case_message)
            if changing_gear_case_message:
                print ('ChangingGearCase: {0}').format(changing_gear_case_message)
            print


        ###########################################
        ### Waits for the period for every loop ###
        ###########################################
        if SHOULD_SEND:
            time.sleep(PERIOD)

    #########################################
    ### It's time to generate the report  ###
    #########################################
    strong_break_case_report = strong_break_case.generate_report()
    changing_gear_case_report = changing_gear_case.generate_report()
    print (strong_break_case_report)
    print (changing_gear_case_report)

    # Initializing the Communication class
    if SHOULD_SEND:
        sender.finish_process(FINISH_COMMAND)

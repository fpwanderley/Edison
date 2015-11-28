# Detects and show a report about the case where the driver is pressing the break pedal
# strongly.
LIMITS_INTERVALS = [(0.0, -2.5), (-2.5, -5.0), (-5.0, -9.8), (-9.8, -30.0)]
LIMIT_CATEGORIES = ['NORMAL LIMIT-(0.0, -2.5)', 'YELLOW ATTENTION-(-2.5, -5.0)',
                    'RED LIMIT-(-5.0, -9.8)', 'ARE YOU CRAZY?!-(-9.8, -30.0)']

COLORS = {
    'NORMAL LIMIT-(0.0, -2.5)': '#009a00',
    'YELLOW ATTENTION-(-2.5, -5.0)': '#FFFF00',
    'RED LIMIT-(-5.0, -9.8)': '#FF0000',
    'ARE YOU CRAZY?!-(-9.8, -30.0)': '#a6a6a6'
}

break_analysis_file_path = 'BreakAnalysis.txt'

class Acceleration:
    def __init__(self, acceleration):
        self.acceleration = float(acceleration)
        self.set_category(acceleration = self.acceleration)

    def set_category(self, acceleration):
        if acceleration > 0:
            self.category = None
        else:
            for idx, interval in enumerate(LIMITS_INTERVALS):
                min_interval = interval[0]
                max_interval = interval[1]

                if min_interval >= acceleration > max_interval:
                    self.category = LIMIT_CATEGORIES[idx]

class StrongBreakCase(object):

    def __init__(self, period):
        self.period = period
        self.entries = []

    def include_new_entry(self, new_entry):
        new_acceleration = Acceleration(new_entry)
        self.entries.append(new_acceleration)

    def get_last_entry(self):
        if self.entries == []:
            return None
        else:
            return self.entries[-1]

    def get_category_for_entry(self, entry):
        return entry.category

    def get_current_message(self, idx = None):

        # idx was not informed. Returns the status for the last entry.
        if not idx:
            return self.get_category_for_entry(self.get_last_entry())
        else:
            return self.get_category_for_entry(self.entries[idx])

    def get_correct_entries(self, entries):
        return [acce for acce in entries if acce.category != None ]

    def generate_report(self):
        from collections import Counter
        correct_entries = self.get_correct_entries(entries=self.entries)
        category_list = [acc.category for acc in correct_entries]
        category_list_len = len(category_list)
        counter = Counter(category_list)
        frac_dict = {key: value*100/category_list_len for key, value in counter.items()}
        return frac_dict


# def StrongBreakCase(acceleration_list, period):
#
#     class Acceleration:
#         def __init__(self, acceleration):
#             self.acceleration = acceleration
#             self.set_category(acceleration = acceleration)
#
#         def set_category(self, acceleration):
#             if acceleration > 0:
#                 return
#             else:
#                 for idx, interval in enumerate(LIMITS_INTERVALS):
#                     min_interval = interval[0]
#                     max_interval = interval[1]
#
#                     if min_interval >= acceleration > max_interval:
#                         self.category = LIMIT_CATEGORIES[idx]
#
#         @classmethod
#         def transform_accelerations_to_text(cls, accelerations):
#             text = []
#             for acceleration in negative_accelerations:
#                 text.append(str(acceleration.category) + ': ' + str(acceleration.acceleration))
#             return '\n'.join(text)
#
#         @classmethod
#         def get_category_fracs_from_accelerations(cls, acc_list):
#             from collections import Counter
#             category_list = [acc.category for acc in acc_list]
#             category_list_len = len(category_list)
#             counter = Counter(category_list)
#             frac_dict = {key: value*100/category_list_len for key, value in counter.items()}
#             return frac_dict
#
#         @classmethod
#         def prepare_parameters_for_pie_chart(cls, fracs_dict, colors_dict):
#             fracs = []
#             colors = []
#             explode = (0, 0, 0, 0)
#             labels = []
#
#             for key, value in fracs_dict.items():
#                 fracs.append(value)
#                 labels.append(key)
#                 colors.append(colors_dict[key])
#
#             return fracs, colors, explode, labels
#
#         #########################
#         ### GRAPHS GENERATORS ###
#         #########################
#
#         @classmethod
#         def generate_pie_chart(cls, negative_accelerations):
#             fracs_dict = Acceleration.get_category_fracs_from_accelerations(negative_accelerations)
#             fracs, colors, explode, labels = Acceleration.prepare_parameters_for_pie_chart(fracs_dict, COLORS)
#             create_pie_chart_from_data(fracs=fracs, colors=colors, explode=explode, labels=labels)
#
#         @classmethod
#         def generate_histogram(cls, acceleration_list, period):
#             # Creating a Histogram to analysis.
#             acceleration_to_histogram = [acc if acc < 0 else 0.0 for acc in acceleration_list]
#             create_histogram_from_data(acceleration_to_histogram, period = period, x_label = 'Segundos', y_label = 'Aceleração')
#
#     negative_accelerations = []
#     acceleration_list = [float(x) for x in acceleration_list]
#     for acceleration in acceleration_list:
#         if acceleration < 0:
#             negative_accelerations.append(Acceleration(acceleration=acceleration))
#
#     Acceleration.generate_histogram(acceleration_list=acceleration_list, period=period)
#     Acceleration.generate_pie_chart(negative_accelerations=negative_accelerations)
#
#     content_to_print = Acceleration.transform_accelerations_to_text(accelerations=negative_accelerations)
#     FileWriter(break_analysis_file_path, content_to_print)
# -*- coding: utf-8 -*-
# Detects and show a report about the case where the driver is pressing the break pedal
# strongly.
BREAK_INTERVALS = [(0.0, -5.0), (-5.0, -9.8), (-9.8, -30.0)]
BREAK_CATEGORIES = ['NORMAL LIMIT-(0.0, -5.0)', 'YELLOW LIMIT-(-5.0, -9.8)',
                    'RED LIMIT-(-9.8, -30.0)']

GEAR_INTERVALS = [(0, 1000), (1000, 2000), (2000, 7000)]
GEAR_CATEGORIES = ['NORMAL LIMIT-(0, 1000)', 'YELLOW LIMIT-(1000, 2000)',
                    'RED LIMIT-(2000, 7000)']

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
        """ Atrela uma categoria para a aceleraçao.

        Inclui uma categoria para a aceleraçao apenas em caso de esta ser negativa.

        :param acceleration: Float com o valor da aceleraçao.
        :return: None
        """
        if acceleration > 0:
            self.category = None
        else:
            for idx, interval in enumerate(BREAK_INTERVALS):
                min_interval = interval[0]
                max_interval = interval[1]

                if min_interval >= acceleration > max_interval:
                    self.category = BREAK_CATEGORIES[idx]

class StrongBreakCase(object):

    def __init__(self, period):
        self.period = period
        self.entries = []

    def include_new_entry(self, new_entry):
        """ Inclui uma nova Acceleration na lista self.entries.

        :param new_entry: Float com o valor da aceleraçao.
        :return: None
        """
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
        """ Retorna a informaçao a respeito de uma entrada.

        :param idx: Indice de entradas a ser consultado.
        :return: String com a categoria da entrada.
        """

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

class GearChanging(object):

    def __init__(self, previous_rpm_derivative, current_rpm_derivative, rpm, period, speed):
        self.was_read = False
        self.is_gear_changing = False
        self.rpm = rpm
        self.previous_rpm_derivative = previous_rpm_derivative
        self.current_rpm_derivative = current_rpm_derivative
        self.period = period
        self.speed = speed

        self.analyse_changing_gear()

    def analyse_changing_gear(self):
        """ Analisa se houve ou nao uma troca de marcha, e a categoriza.

        Caso for uma troca de marcha, self.is_gear_changing = True

        :return: None
        """

        def is_close_to_zero(value):
            MARGEM = 10.0
            CENTRO = 0.0

            LOWER_LIMIT = (CENTRO - MARGEM)
            UPPER_LIMIT = (CENTRO + MARGEM)

            value = float(value)
            if ((value >= LOWER_LIMIT) and (value <= UPPER_LIMIT)):
                return True
            return False

        if ((self.previous_rpm_derivative > 0 and self.current_rpm_derivative <= 0) and self.rpm > 500):
            self.is_gear_changing = True

            self.set_category()

    def set_category(self):
        """ Seta a categoria de troca de marcha.

        De acordo com a quantidade de RPM's do momento em que houve a troca de marcha,
        a categoria será definida.

        :return: None
        """

        rpm = int(self.rpm)

        for idx, interval in enumerate(GEAR_INTERVALS):
            min_interval = interval[0]
            max_interval = interval[1]

            if min_interval <= rpm < max_interval:
                self.category = GEAR_CATEGORIES[idx]
                return

    def __str__(self):
        return ('Categoria: {0}; Velocidade: {1}; RPM: {2}').format(self.category,
                                                                    self.speed,
                                                                    self.rpm)

class CorrectGearChangingCase(object):

    def __init__(self, period):
        self.period = period
        self.entries = []
        self.last_rpm_derivative = None

    def include_new_entry(self, rpm_derivative, rpm, speed):
        """ Inclui uma nova troca de marcha nas entradas.

        :param rpm_derivative: Variaçao atual do RPM.
        :param rpm: Valor atual do RPM.
        :return: None
        """

        # Inicializa a variaçao do rpm.
        if not self.last_rpm_derivative:
            self.last_rpm_derivative = rpm_derivative

        gear_changing_candidate = GearChanging(previous_rpm_derivative=self.last_rpm_derivative,
                                               current_rpm_derivative=rpm_derivative,
                                               rpm=rpm,
                                               period=self.period,
                                               speed=speed)

        if gear_changing_candidate.is_gear_changing:
            self.entries.append(gear_changing_candidate)

        # Atualiza a última variação de RPM.
        self.last_rpm_derivative = rpm_derivative

    def get_current_message(self):
        """ Retorna a troca de marcha ainda nao lida.

        Deve retornar None em caso de nao haver troca de marcha nao lida.

        :return: GearChanging or None
        """

        last_gear_changing = self.get_last_gear_changing()

        if last_gear_changing:
            if not last_gear_changing.was_read:
                # Updates the was_read atribute and re-append it to the self.entries list.
                last_gear_changing.was_read = True
                self.set_last_gear_changing(new_gear_changing=last_gear_changing)

                return last_gear_changing
        return None

    def set_last_gear_changing(self, new_gear_changing):
        """ Atualiza a ultima entrada de self.entries

        :param new_gear_changing: A nova GearChanging.
        :return: True em caso de sucesso, e False em caso de falha.
        """

        if len(self.entries) > 0:
            self.entries[-1] = new_gear_changing
            return True
        return False

    def get_last_gear_changing(self):
        """ Retorna ultima troca de marcha presente em self.entries.

        :return: GearChanging or None
        """
        if len(self.entries) > 0:
            return self.entries[-1]
        return None

    def generate_report(self):
        from collections import Counter
        correct_entries = self.entries
        category_list = [gear.category for gear in correct_entries]
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
#                 for idx, interval in enumerate(BREAK_INTERVALS):
#                     min_interval = interval[0]
#                     max_interval = interval[1]
#
#                     if min_interval >= acceleration > max_interval:
#                         self.category = BREAK_CATEGORIES[idx]
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


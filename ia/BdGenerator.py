# -*- coding: utf-8 -*-

from random import *

BREAK_CLASSIFICATIONS = ['green(0 -> -1 m/s2)', 'yellow(-1 -> -2 m/s2)', 'red(-1 -> -2 m/s2)']
GEAR_CLASSIFICATIONS = ['green(0 -> 1000 RPM)', 'yellow(1000 -> 2000 RPM)', 'red(2000 -> 7000 RPM)']

ANALYSIS_SEQUENCE = ['break', 'gear']

ANALYSIS = {
    'break': BREAK_CLASSIFICATIONS,
    'gear': GEAR_CLASSIFICATIONS
}

def generate_all_feature_values(analysis_list=None, total_of_entries=1):

    analysis_list = ANALYSIS
    generated_entries = []

    for i in range(total_of_entries):

        generated_elements = {}

        # Para cada analise, deve gerar valores que sejam 100 no total.
        for key, analysis in analysis_list.iteritems():

            # Cria uma nova entrada no dict de saida.
            generated_elements[key] = {}
            analysis_dict = generated_elements[key]

            total_generated = 0
            total_classifications = len(analysis)

            # Apenas gera pra len - 1. O ultimo é o que falta pra 100.
            for idx in range(total_classifications - 1):
                # import pdb;pdb.set_trace()
                random_value = uniform(0, 100-total_generated)
                new_entry_name = analysis[idx]

                # Cria a entrada no dict de saida.
                analysis_dict[new_entry_name] = random_value

                # Atualiza o total gerado.
                total_generated = total_generated + random_value

            # Para o ultimo elemento.
            random_value = 100 - total_generated
            new_entry_name = analysis[-1]

            # Cria a entrada no dict de saida.
            analysis_dict[new_entry_name] = random_value

        generated_entries.append(generated_elements)
    return generated_entries

def send_generated_feature_to_file(generated_feature, analysis_list=ANALYSIS):

    with open("training_space.txt", "w+") as f:

        # Criando o header.
        for analysis_key in ANALYSIS_SEQUENCE:
            classification_list = analysis_list[analysis_key]

            for classification in classification_list:

                string_to_write = analysis_key + '_' + classification + '\t'

                f.write(string_to_write)

        f.write('\n')

        for entrie in generated_feature:
            # Preenchendo com os valores
            for analysis_key in ANALYSIS_SEQUENCE:

                classification_list = analysis_list[analysis_key]

                for classification in classification_list:

                    generated_value = entrie[analysis_key][classification]
                    string_to_write = str(generated_value) + '\t'

                    f.write(string_to_write)

                header_created = True

            f.write('\n')





# According to period and the list_length this function creates a list with:
# - Same length of list_lenght.
# - Each of its values is equal to: period*element_index_in_the_list
def build_x_axis_values(period, list_lenght):

    # x_axis = [str(round(idx*period, 1)) for idx in range(list_lenght)]
    x_axis = [round(idx*period, 1) for idx in range(list_lenght)]
    return x_axis

def plot_graphs(log_dicts, x_axis, data_labels=None):
    import matplotlib.pyplot as plt

    DATA_LABELS = ['RPM', 'SPEED', 'THROTTLE']
    DATA_LABELS = ['RPM_DERIVATIVE']

    if data_labels:
        DATA_LABELS = data_labels

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

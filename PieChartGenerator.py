"""
Make a pie charts of varying size - see
http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.pie for the docstring.

This example shows a basic pie charts with labels optional features,
like autolabeling the percentage, offsetting a slice with "explode"
and adding a shadow, in different sizes.

"""
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

def create_pie_chart_from_data(fracs, colors, explode, labels):

    # Separa as partições
    pie = plt.subplot()
    pie.set_label('Teste')

    plt.pie(fracs, explode = explode,
            colors = colors, labels = labels,
            autopct = '%1.1f%%', shadow = True)

    plt.show()
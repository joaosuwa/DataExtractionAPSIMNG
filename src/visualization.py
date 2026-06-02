import matplotlib.pyplot as plt
import numpy as np
import os

def bar_plot(x, y, directory="output/images", file_name="graph", file_format='', acumulated=False, title=None, xlabel=None, ylabel=None):
    if acumulated:
        y = np.cumsum(y)
    plt.bar(x, y)
    if title:
        plt.title(title)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)
    if file_format is None:
        file_format = "png"

    plt.bar(x, y, width=1, edgecolor='white', linewidth=0.7)

    if not os.path.exists(directory):
        os.makedirs(directory)

    plt.savefig(f"{directory}/{file_name}{file_format}", dpi=300)

bar_plot([1, 2, 3], [4, 5, 6], file_name="example", title="Example Bar Plot", xlabel="X-axis", ylabel="Y-axis", file_format=".pdf")
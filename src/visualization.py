import matplotlib.pyplot as plt
import numpy as np
import os
from itertools import cycle

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
    plt.close()

def line_plot(x, y, directory="output/images", file_name="graph", file_format='.png', title=None, xlabel=None, ylabel=None):
    
    colors = cycle(plt.rcParams['axes.prop_cycle'].by_key()['color'])
    fig, ax = plt.subplots()

    if title:
        plt.title(title)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)

    # Verifica se y contém múltiplas listas (ex: y = [[1, 2], [3, 4]])
    if isinstance(y[0], (list, tuple)):
        for y_axis in y:
            if len(x) != len(y_axis):
                raise ValueError("O tamanho de 'x' deve ser igual ao tamanho de cada lista dentro de 'y'.")
            ax.plot(x, y_axis, color=next(colors))
            
    # Caso y seja apenas uma lista simples (uma única linha)
    else:
        if len(x) != len(y):
            raise ValueError("x e y devem ter o mesmo tamanho.")
        ax.plot(x, y, color=next(colors))

    if not os.path.exists(directory):
        os.makedirs(directory)

    plt.savefig(f"{directory}/{file_name}{file_format}", dpi=300)
    plt.close(fig)
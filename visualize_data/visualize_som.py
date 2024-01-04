import numpy as np
from matplotlib import pyplot as plt


def plot_som_series_averaged_center(som_x, som_y, win_map, file_name=None):
    fig, axs = plt.subplots(som_x, som_y, figsize=(15, 15))
    fig.suptitle('Clusters')
    for x in range(som_x):
        for y in range(som_y):
            cluster = (x, y)
            if cluster in win_map.keys():
                for series in win_map[cluster]:
                    axs[cluster].plot(series, c="gray", alpha=0.5)
                axs[cluster].plot(np.average(np.vstack(win_map[cluster]), axis=0), c="blue")
            cluster_number = x * som_y + y + 1
            axs[cluster].set_title(f"Cluster {cluster_number}")

    if file_name is not None:
        plt.savefig(file_name)
    else:
        plt.show()


def multiple_plot_som_series_averaged_center(som_x, som_y, win_maps, file_name=None, color: list = None):
    fig, axs = plt.subplots(som_x, som_y, figsize=(20, 20))
    fig.suptitle('Clusters')
    for i in range(len(win_maps)):
        for x in range(som_x):
            for y in range(som_y):
                cluster = (x, y)
                if cluster in win_maps[i].keys():
                    axs[cluster].plot(np.average(np.vstack(win_maps[i][cluster]), axis=0), c=color[i])
                cluster_number = x * som_y + y + 1
                axs[cluster].set_title(f"Cluster {cluster_number}")
    fig.legend([f"It. {i + 1}" for i in range(len(win_maps))], loc='upper center', #bbox_to_anchor=(0.5, 1.05),
               ncol=3, fancybox=True, shadow=True)

    if file_name is not None:
        plt.savefig(file_name)
    else:
        plt.show()
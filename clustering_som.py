import importlib

import pandas as pd
import numpy as np
import math
from matplotlib import pyplot as plt
import pickle

from sklearn.metrics import davies_bouldin_score, silhouette_score
from preprocessing_data import utils
import minisom

from visualize_data import visualize_som

from GlobalLandTemperatures.visualize_data import visualization

df = pd.read_csv("processed_data.csv")
df_group = df.groupby("Country", group_keys=True)
time_series = []
for (country, data) in df_group:
        time_series.append(data["AverageTemperature"].values)

time_series = np.array(time_series)
X = time_series[:, -120:]

plt.ion()
plt.rcParams.update({'font.size': 20})


som_x = 3
som_y = 3
som = minisom.MiniSom(som_x, som_y, input_len=len(X[0]), sigma=0.3, learning_rate=0.3)

som.random_weights_init(X)
som.train(X, 500_000)

win_map = som.win_map(X)

visualize_som.plot_som_series_averaged_center(som_x, som_y, win_map, "Som.png")


win_maps = []
soms = []

for i in range(3):
    s = minisom.MiniSom(som_x, som_y, input_len=120, sigma=0.3, learning_rate=0.3)
    s.random_weights_init(X)
    s.train(X, 500_000)
    soms.append(s)

    win_maps.append(s.win_map(X))

colors = ['blue', 'yellow', 'green', 'orange', 'brown']
# hien thi 3 lan som
visualize_som.multiple_plot_som_series_averaged_center(som_x, som_y, win_maps, color=colors, file_name="Som_3it.png")


size_x = [2, 3, 4, 5]
size_y = [2, 3, 4, 5]
partitions = []

for i in range(4):
    temp = []
    s = minisom.MiniSom(size_x[i], size_y[i], input_len=120, sigma=0.3, learning_rate=0.3)
    s.random_weights_init(X)
    s.train(X, 500_000)

    for x in X:
        temp.append(s.activate(x).argmin())
    partitions.append(temp)


dbis = []
shs = []
for i in range(len(partitions)):
    dbis.append(davies_bouldin_score(X, partitions[i]))
    shs.append(silhouette_score(X, partitions[i]))


for i in range(len(partitions)):
    print(f"Som {size_x[i]}x{size_y[i]}: DBI - {dbis[i]}, SH - {shs[i]}")

input("Press enter to exit")
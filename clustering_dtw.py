import importlib

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import pickle

from tslearn.clustering import TimeSeriesKMeans

from sklearn.metrics import davies_bouldin_score, silhouette_score

from preprocessing_data import utils

from GlobalLandTemperatures.visualize_data import visualization

df = pd.read_csv("processed_data.csv")
df_group = df.groupby("Country", group_keys=True)
time_series = []

for (country, data) in df_group:
    if country != "Vietnam":
        time_series.append(data["AverageTemperature"].values)

time_series = np.array(time_series)
X = time_series[:, -120:]

time_series_vn = df_group.get_group("Vietnam")["AverageTemperature"].values.reshape(1, -1)[:, -120:]

plt.ion()
plt.rcParams.update({'font.size': 15})

center_clusters_euclid = []
center_clusters_dtw = []
center_clusters_itakura = []
center_clusters_sakoe = []
labels_dtw, labels_euclid, labels_itakura, labels_sakoe = [], [], [], []

for i in range(2, 6):

    kmeans_euclid = TimeSeriesKMeans(n_clusters=i, metric='euclidean')
    kmeans_euclid.fit(X)
    center_clusters_euclid.append(kmeans_euclid.cluster_centers_.reshape(-1, 120))
    labels_euclid.append(kmeans_euclid.predict(X))
    kmeans_euclid.predict(time_series_vn)


    kmeans_dtw = TimeSeriesKMeans(n_clusters=i, metric='dtw')
    kmeans_dtw.fit(X)
    center_clusters_dtw.append(kmeans_dtw.cluster_centers_.reshape(-1, 120))
    labels_dtw.append(kmeans_dtw.predict(X))

    for j in range(1, 4):
        kmeans_itakura = TimeSeriesKMeans(n_clusters=i, metric='dtw', metric_params = {"global_constraint": "itakura", "itakura_max_slope": 1.0 * j} )
        kmeans_itakura.fit(X)
        center_clusters_itakura.append(kmeans_itakura.cluster_centers_.reshape(-1, 120))
        labels_itakura.append(kmeans_itakura.predict(X))

    for j in range(1, 4):
        kmeans_sakoe_chiba = TimeSeriesKMeans(n_clusters=i, metric='dtw', metric_params = {"global_constraint": "sakoe_chiba", "sakoe_chiba_radius": 5 * j} )
        kmeans_sakoe_chiba.fit(X)
        center_clusters_sakoe.append(kmeans_sakoe_chiba.cluster_centers_.reshape(-1, 120))
        labels_sakoe.append(kmeans_sakoe_chiba.predict(X))

#sap xep cum theo gia tri trung binh
utils.sort_3d_avg(center_clusters_euclid, axis=1)
utils.sort_3d_avg(center_clusters_dtw, axis=1)
utils.sort_3d_avg(center_clusters_itakura, axis=1)
utils.sort_3d_avg(center_clusters_sakoe, axis=1)

y_labels = ["n = 2", "n = 3", "n = 4", "n = 5"]

visualization.multiple_plot(center_clusters_euclid, 4, 1, "Kmeans Euclid")
visualization.multiple_plot(center_clusters_dtw, 4, 1, "DTW", y_labels)
visualization.multiple_plot(center_clusters_itakura, 4, 3, "DTW Itakura", y_labels, ["s = 1.0", "s = 2.0", "s = 3.0"])
visualization.multiple_plot(center_clusters_sakoe, 4, 3, "DTW Sakoe-Chiba", y_labels, ["r = 5", "r = 10", "r = 15"])


#plot chuoi cua viet nam
visualization.line_plot(time_series_vn.T)

# danh gia mo hinh voi cac metric khac

dbs_dtw, dbs_itakura, dbs_sakoe, dbs_euclid = [], [], [], []
sh_dtw , sh_itakura, sh_sakoe, sh_euclid = [], [], [], []

for i in range(len(labels_dtw)):
    dbs_dtw.append(davies_bouldin_score(X, labels_dtw[i]))
    dbs_euclid.append(davies_bouldin_score(X, labels_euclid[i]))

    sh_dtw.append(silhouette_score(X, labels_dtw[i]))
    sh_euclid.append(silhouette_score(X, labels_euclid[i]))


for i in range(len(labels_sakoe)):
    dbs_itakura.append(davies_bouldin_score(X, labels_itakura[i]))
    dbs_sakoe.append(davies_bouldin_score(X, labels_sakoe[i]))

    sh_itakura.append(silhouette_score(X, labels_itakura[i]))
    sh_sakoe.append(silhouette_score(X, labels_sakoe[i]))



for i in range(len(labels_dtw)):
    print(f"n = {i + 2} DBS DTW: {dbs_dtw[i]} DBS EUCLID: {dbs_euclid[i]}")

for i in range(len(labels_dtw)):
    print(f"n = {i + 2} SH DTW: {sh_dtw[i]} SH EUCLID: {sh_euclid[i]}")

for i in range(len(labels_sakoe)):
    print(f"n = {i // 3 + 2} r = {5 *(i % 3 + 1)} DBS SAKOE: {dbs_sakoe[i]} s = {1.0 *(i % 3 + 1)} DBS ITAKURA: {dbs_itakura[i]}")

for i in range(len(labels_sakoe)):
    print(f"n = {i // 3 + 2} r = {5 *(i % 3 + 1)} SH SAKOE: {sh_sakoe[i]} s = {1.0 *(i % 3 + 1)} SH ITAKURA: {sh_itakura[i]}")


input("Press enter to exit")

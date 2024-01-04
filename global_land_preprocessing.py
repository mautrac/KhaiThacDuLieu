import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import pandas as pd

from preprocessing_data import utils
from preprocessing_data import statis
from GlobalLandTemperatures.visualize_data import visualization


df = pd.read_csv("GlobalLandTemperaturesByCountry.csv")
df['dt'] = df['dt'].apply(utils.transform_date_format)

cols = df.columns
countries = df['Country'].unique()

#date format for matplot
xfmt = mdates.DateFormatter('%Y-%m')

records_by_country, null_records_by_country = statis.statis_by_column(df, 'Country')
plt.ion()
visualization.bar_plot(records_by_country.values(), null_records_by_country.values(), color=['b', 'r'], xlabel='Country'
                       , ylabel='Records', keep_x_axis=False, legend_name=['No. of Records', 'No. of Null Records']
                       )

df['dt'] = df['dt'].apply(utils.date_to_num)

null_index = statis.get_null_index(df)
null_df = df.loc[null_index.values]

group_data = df.groupby("Country", group_keys=True)
vietnam_df = group_data.get_group("Vietnam")
visualization.line_plot(vietnam_df["dt"], vietnam_df["AverageTemperature"], "Average Temp", x_formatter=xfmt)

visualization.scatter_plot([df['dt'].values, df["Country"].values], [null_df['dt'].values, null_df["Country"].values],
                           figsize=(15, 40), size=[0.5, 0.5], color=['b', 'r'], xlabel="Time", ylabel="Country",
                           legend_name=["No. of Records", "No. of Null Records"], x_formatter=xfmt
                           )

threshold = utils.date_to_num("1900-01")
df = df[df['dt'] > threshold]
null_df = null_df[null_df['dt'] > threshold]


visualization.scatter_plot([df['dt'].values, df['Country'].values], [null_df['dt'].values, null_df['Country'].values],
                           figsize=(15, 40), size=[0.5, 0.5], color=['b', 'r'], xlabel="Time", ylabel="Country",
                           legend_name=["No. of Records", "No. of Null Records"], x_formatter=xfmt,
                           file_name="country_records.png"
                           )

records_by_country, null_records_by_country = statis.statis_by_column(df, 'Country')
visualization.bar_plot(records_by_country.values(), null_records_by_country.values(), color=['b', 'r'], xlabel='Country'
                       , ylabel='Records', keep_x_axis=False, legend_name=['No. of Records', 'No. of Null Records']
                       )

drop_countries = []
record_threshold = 1364
for (country, records) in records_by_country.items():
    if records < record_threshold:
        drop_countries.append(country)

df = df[ ~df["Country"].isin(drop_countries) ]
records_by_country, null_records_by_country = statis.statis_by_column(df, 'Country')
visualization.bar_plot(records_by_country.values(), null_records_by_country.values(), color=['b', 'r'], xlabel='Country'
                       , ylabel='Records', keep_x_axis=False, legend_name=['No. of Records', 'No. of Null Records']
                       )

processed_df = df.interpolate()
records_by_country, null_records_by_country = statis.statis_by_column(processed_df, 'Country')
visualization.bar_plot(records_by_country.values(), null_records_by_country.values(), color=['b', 'r'], xlabel='Country'
                       , ylabel='Records', keep_x_axis=False, legend_name=['No. of Records', 'No. of Null Records']
                       )

#bo cot dt
processed_df.drop(columns="dt", inplace=True)
processed_df.to_csv("./processed_data.csv", index=False)








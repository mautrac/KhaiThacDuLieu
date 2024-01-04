import pandas as pd


def get_null_index(df: pd.DataFrame):
    null_index = df.isnull().any(axis=1)
    return df[null_index].index


def statis_by_column(df: pd.DataFrame, column_name: str):
    if not isinstance(df, pd.DataFrame):
        raise "Data is not DataFrame"

    all_column_names = df.columns
    if not all_column_names.__contains__(column_name):
        raise "Invalid column name"

    group_data = df.groupby("Country", group_keys=True)

    records_by_group_dict = dict()
    null_records_by_group = dict()
    for g in group_data:
        records_by_group_dict[g[0]] = len(g[1])
        null_records_by_group[g[0]] = len(get_null_index(g[1]) )

    return records_by_group_dict, null_records_by_group

from datetime import datetime
import matplotlib.dates as mdates
import numpy as np


def transform_date_format(input_date_string, format = "%Y-%m"):
    try:
        date_object = datetime.strptime(input_date_string, "%Y-%m-%d")
        return date_object.strftime(format)
    except ValueError:
        pass

    try:
        date_object = datetime.strptime(input_date_string, "%m/%d/%Y")
        return date_object.strftime(format)
    except ValueError:
        raise ValueError("Invalid date format")



def date_to_num(input: str, format = "%Y-%m"):
    date = datetime.strptime(input, format)
    num = mdates.date2num(date)
    return num


def sort_3d_avg(arr, axis = 0):
    f = lambda x: np.argsort(np.average(x, axis).ravel(), axis=0)
    for i in range(len(arr)):
        arr[i] = arr[i][f(arr[i])]


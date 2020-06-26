import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px

############################################
# General Annotations
############################################
# Data files are separated by date with name as given by file_name function
# the format of the csv file is the following:
# Unix_Timestamp, Temperature1,


############################################
# Handle data
############################################
# PRE:  date: datetime, date of measurement.
# POST: returns string with file name of data of given feature on given date
def file_name(date):
    path = ''
    name = 'datalog_' + date.strftime("%d_%m_%Y") + '.csv'
    return name


# PRE:  features: list of strings
#       day_start: datetime, first day of imported data
#       day_end: datetime, last day of imported data,
# POST: returns panda with data
def import_data(day_start, day_end):
    delta_days = day_end - day_start
    interval_days = []
    for d in range(delta_days.days+1):
        interval_days.append(day_start + timedelta(days=d))
    # Create list of file names
    file_names = []
    for day in interval_days:
        file_names.append(file_name(day))
    # Create list with pandas of days meas.
    data = []
    for filename in file_names:
        data.append(pd.read_csv(filename))
    df = data[0]
    # Union in single panda
    for dfs in data[0:]:
        df.append(dfs, ignore_index=True)
    # Convert times stamp to datetime format
    df = df.rename(columns={"Unix_Timestamp": "Date_time"})
    df.Date_time = pd.to_datetime(df.Date_time, unit='s')
    return df


# PRE:  dataframe: panda, initial data with a 'time' column
#       period_measurement: int, seconds between one meas and another
#       time_interval_start: int, length in seconds of the time axis for dataset
#       features: list of strings, names of features, should always contain 'Date_time' value
# POST: returns panda with data
def return_dataset_ready(dataframe, period_measurement, time_interval_start, features):
    return dataframe[features].tail(int(1 / float(period_measurement) * time_interval_start))


############################################
# Interactive graphs
############################################

# PRE:  df: panda, initial data with a 'time' column
#       feature: str, name of column of y-Axis,
# POST: returns panda with data
def graph_single_data(dataframe,feature):
    fig = px.line(dataframe, x="Date_time", y=feature, title='Temperature')
    fig.write_html('first_figure.html', auto_open=False)

'''
# Import data
types = {'Time': 'str'}
parse_dates = ['Time']
data = pd.read_csv("dataexport_20200618T105025.csv", dtype=types, parse_dates=parse_dates)
temp = data.Temperature
print(data)

import plotly.express as px

fig = px.line(data, x="Time", y="Temperature", title='Temperature')
fig.write_html('first_figure.html', auto_open=True)
'''
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
    path = 'data/'
    name = path + 'datalog_' + date.strftime("%d_%m_%Y") + '.csv'
    return name


# PRE:  features: list of strings
#       day_start: datetime, first day of imported data
#       day_end: datetime, last day of imported data,
# POST: returns panda with data
def import_data(day_start, day_end):
    delta_days = day_end - day_start
    interval_days = []
    for d in range(delta_days.days + 1):
        interval_days.append(day_start + timedelta(days=d))
    # Create list of file names
    print(interval_days)
    file_names = []
    for day in interval_days:
        file_names.append(file_name(day))
    # Create list with pandas of days meas.
    data = []
    for filename in file_names:
        data.append(pd.read_csv(filename))
    df = data[0]
    # Union in single panda
    for dfs in data[1:]:
        df = df.append(dfs, ignore_index=True)
    # Convert times stamp to datetime format
    df = df.rename(columns={"d_m_Y_H_M_S": "Date_time"})
    df.Date_time = pd.to_datetime(df.Date_time, format="%d_%m_%Y_%H_%M_%S")
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
# POST: returns str of name file
def name_htmldiv_single_graph(dataframe, feature):
    starttsp = int(datetime.timestamp(dataframe.Date_time.iloc[0]))
    endtsp = int(datetime.timestamp(dataframe.Date_time.iloc[-1]))
    name = 'graphs_html_prep/html_div' + feature + '_' + str(starttsp) + '_to_' + str(endtsp) + '.html'
    return name


# PRE:  dataframe: panda, initial data with a 'time' column
#       feature: str, name of column of y-Axis,
#       name: str, want to use output of
# POST: creates html output
def output_htmldiv_single_graph(dataframe, feature):
    filename = name_htmldiv_single_graph(dataframe, feature)
    fig = px.line(dataframe, x="Date_time", y=feature, title='Temperature')
    fig.write_html(file=filename, include_plotlyjs='plotly.js', full_html=False, auto_open=False)


# PRE:  name: str, name of output file
#       *name_graphs: name of the graphs to be included,
# POST:
def create_html_page(name, *names_graphs):
    # open final file in write mode
    with open(name, 'w') as outputfile:
        # open header in read mode and write in output
        with open('basepage_top.html', 'r') as header:
            outputfile.write(header.read())
        for graph_name in names_graphs:
            with open(graph_name, 'r') as graph:
                outputfile.write(graph.read())
        with open('basepage_bottom.html', 'r') as bottom:
            outputfile.write(bottom.read())


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

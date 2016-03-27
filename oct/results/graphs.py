import os
import pytz
import pygal
import numpy as np
import pandas as pd
from dateutil.tz import tzlocal


def get_local_time(index):
    """Localize datetime for better output in graphs

    :param pandas.DateTimeIndex index: pandas datetime index
    :return: aware time objet
    :rtype: datetime.time
    """
    dt = index.to_pydatetime()
    dt = dt.replace(tzinfo=pytz.utc)
    return dt.astimezone(tzlocal()).time()


def resp_graph_raw(dataframe, image_name, dir='./'):
    """Response time graph for raw data

    :param pandas.DataFrame dataframe: the raw results dataframe
    :param str image_name: the output file name
    :param str dir: the output directory
    :return: None
    """
    factor = int(len(dataframe) / 10)
    df = dataframe.reset_index()
    grp = df.groupby(pd.cut(df.index, np.arange(0, len(df), factor)))

    fig = pygal.Dot(stroke=False,
                    x_label_rotation=25,
                    x_title='Elapsed Time In Test (secs)',
                    y_title='Average Response Time (secs)',
                    js=('scripts/pygal-tooltip.min.js',))
    fig.x_labels = [x for x in grp.first()['epoch']]
    fig.title = image_name.split('.')[0]
    fig.add('Time', [x for x in grp.describe()['scriptrun_time'].unstack()['mean'].round(2)])
    fig.render_to_file(filename=os.path.join(dir, image_name))


def resp_graph(dataframe, image_name, dir='./'):
    """Response time graph for bucketed data

    :param pandas.DataFrame dataframe: dataframe containing all data
    :param str image_name: the output file name
    :param str dir: the output directory
    :return: None
    """
    fig = pygal.TimeLine(x_title='Elapsed Time In Test (secs)',
                         y_title='Response Time (secs)',
                         x_label_rotation=25,
                         js=('scripts/pygal-tooltip.min.js',))
    fig.add('AVG', [(get_local_time(index), row['mean'] if pd.notnull(row['mean']) else None)
                    for index, row in dataframe.iterrows()])
    fig.add('90%', [(get_local_time(index), row['90%'] if pd.notnull(row['90%']) else None)
                    for index, row in dataframe.iterrows()])
    fig.add('80%', [(get_local_time(index), row['80%'] if pd.notnull(row['80%']) else None)
                    for index, row in dataframe.iterrows()])
    fig.render_to_file(filename=os.path.join(dir, image_name))


def tp_graph(dataframe, image_name, dir='./'):
    """Throughput graph

    :param pandas.DataFrame dataframe: dataframe containing all data
    :param str dir: the output directory
    :return: None
    """
    fig = pygal.TimeLine(x_title='Elapsed Time In Test (secs)',
                         x_label_rotation=25,
                         y_title='Transactions Per Second (count)',
                         human_readable=True,
                         js=('scripts/pygal-tooltip.min.js',))
    fig.add('Transactions per second', [(get_local_time(index), row['count'])
                                        for index, row in dataframe.iterrows()])
    fig.render_to_file(filename=os.path.join(dir, image_name))

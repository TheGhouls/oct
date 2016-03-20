import os
import pygal
from datetime import time
import pandas as pd


def resp_graph_raw(nested_resp_list, image_name, dir='./'):
    """Response time graph for raw data

    :param nested_resp_list list: the list containing all data
    :param image_name str: the output file name
    :param dir str: the output directory
    :return: None
    """
    fig = pygal.XY(stroke=False, x_title='Elapsed Time In Test (secs)',
                   y_title='Response Time (secs)',
                   js=('http://kozea.github.io/pygal.js/2.0.x/pygal-tooltips.min.js',))
    fig.title = image_name.split('.')[0]
    fig.add('Time', [(round(item[0], 2), round(item[1], 2)) for item in nested_resp_list])
    fig.x_labels = map(str, range(1, len([item[1] for item in nested_resp_list]) + 1))
    fig.render_to_file(filename=os.path.join(dir, image_name))


def resp_graph(dataframe, image_name, dir='./'):
    """Response time graph for bucketed data

    :param dataframe pandas.DataFrame: dataframe containing all data
    :param image_name str: the output file name
    :param dir str: the output directory
    :return: None
    """
    fig = pygal.TimeLine(x_title='Elapsed Time In Test (secs)',
                         y_title='Response Time (secs)',
                         x_label_rotation=25,
                         js=('http://kozea.github.io/pygal.js/2.0.x/pygal-tooltips.min.js',))
    fig.add('AVG', [(index.to_pydatetime().time(), row['mean'] if pd.notnull(row['mean']) else None) for index, row in dataframe.iterrows()])
    fig.add('90%', [(index.to_pydatetime().time(), row['90%'] if pd.notnull(row['90%']) else None) for index, row in dataframe.iterrows()])
    fig.add('80%', [(index.to_pydatetime().time(), row['80%'] if pd.notnull(row['80%']) else None) for index, row in dataframe.iterrows()])
    fig.render_to_file(filename=os.path.join(dir, image_name))


def tp_graph(dataframe, image_name, dir='./'):
    """Throughput graph

    :param dataframe pandas.DataFrame: dataframe containing all data
    :param dir str: the output directory
    :return: None
    """
    fig = pygal.TimeLine(x_title='Elapsed Time In Test (secs)', y_title='Transactions Per Second (count)',
                         human_readable=True, js=('http://kozea.github.io/pygal.js/2.0.x/pygal-tooltips.min.js',))
    fig.add('Transactions per second', [(index.to_pydatetime().time(), row['count'])
                                        for index, row in dataframe.iterrows()])
    fig.render_to_file(filename=os.path.join(dir, image_name))

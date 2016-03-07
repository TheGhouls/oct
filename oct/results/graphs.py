import os
import pygal


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


def resp_graph(avg_resptime_points_dict, percentile_80_resptime_points_dict,
               percentile_90_resptime_points_dict, image_name, dir='./'):
    """Response time graph for bucketed data

    :param avg_resptime_points_dict dict: a dictionnary containing the average response time points
    :param percentile_80_resptime_points_dict dict: a dictionnary containing the percentile 80 response time points
    :param percentile_90_resptime_points_dict dict: a dictionnary containing the percentile 90 response time points
    :param image_name str: the output file name
    :param dir str: the output directory
    :return: None
    """
    fig = pygal.XY(human_readable=True, x_title='Elapsed Time In Test (secs)',
                   y_title='Response Time (secs)',
                   js=('http://kozea.github.io/pygal.js/2.0.x/pygal-tooltips.min.js',))
    x_seq = sorted(avg_resptime_points_dict.keys())
    fig.add('AVG', [(0, None)] + [(round(x, 2), round(avg_resptime_points_dict[x], 2)) for x in x_seq])
    x_seq = sorted(percentile_90_resptime_points_dict.keys())
    fig.add('90pct', [(0, None)] + [(round(x, 2), round(percentile_90_resptime_points_dict[x], 2)) for x in x_seq])
    x_seq = sorted(percentile_80_resptime_points_dict.keys())
    fig.add('80pct', [(0, None)] + [(round(x, 2), round(percentile_80_resptime_points_dict[x], 2)) for x in x_seq])
    fig.render_to_file(filename=os.path.join(dir, image_name))


def tp_graph(throughputs_dict, image_name, dir='./'):
    """Throughput graph

    :param throughputs_dict dict: a dictionary containing the throughputs points
    :param dir str: the output directory
    :return: None
    """
    fig = pygal.XY(x_title='Elapsed Time In Test (secs)', y_title='Transactions Per Second (count)',
                   human_readable=True, js=('http://kozea.github.io/pygal.js/2.0.x/pygal-tooltips.min.js',))
    x_seq = sorted(throughputs_dict.keys())
    y_seq = [round(throughputs_dict[x], 2) for x in x_seq]
    fig.add('Transactions per second', [(None, 0)] + list(zip(x_seq, y_seq)))
    fig.render_to_file(filename=os.path.join(dir, image_name))

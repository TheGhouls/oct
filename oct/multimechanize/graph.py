import os
import pygal

# response time graph for raw data
def resp_graph_raw(nested_resp_list, image_name, dir='./'):
    fig = pygal.XY(stroke=False, x_title='Elapsed Time In Test (secs)', y_title='Response Time (secs)', js=('http://kozea.github.io/pygal.js/2.0.x/pygal-tooltips.min.js',))
    fig.title = image_name.split('.')[0]
    fig.add('Time', [(item[0], item[1]) for item in nested_resp_list])
    fig.render_to_file(filename=dir + image_name)
    fig.x_labels = map(str, range(1, len([item[1] for item in nested_resp_list]) + 1))
    fig.render_to_file(filename=os.path.join(dir, image_name))


# response time graph for bucketed data
def resp_graph(avg_resptime_points_dict, percentile_80_resptime_points_dict, percentile_90_resptime_points_dict, image_name, dir='./'):
    fig = pygal.XY(human_readable=True, x_title='Elapsed Time In Test (secs)', y_title='Response Time (secs)', js=('http://kozea.github.io/pygal.js/2.0.x/pygal-tooltips.min.js',))
    x_seq = sorted(avg_resptime_points_dict.keys())
    fig.add('AVG', [(0, None)] + [(x, avg_resptime_points_dict[x]) for x in x_seq])
    x_seq = sorted(percentile_90_resptime_points_dict.keys())
    fig.add('90pct', [(0, None)] + [(x, percentile_90_resptime_points_dict[x]) for x in x_seq])
    x_seq = sorted(percentile_80_resptime_points_dict.keys())
    fig.add('80pct', [(0, None)] + [(x, percentile_80_resptime_points_dict[x]) for x in x_seq])
    fig.render_to_file(filename=os.path.join(dir, image_name))


# throughput graph
def tp_graph(throughputs_dict, image_name, dir='./'):
    fig = pygal.XY(x_title='Elapsed Time In Test (secs)', y_title='Transactions Per Second (count)',
                   human_readable=True, js=('http://kozea.github.io/pygal.js/2.0.x/pygal-tooltips.min.js',))
    x_seq = sorted(throughputs_dict.keys())
    fig.add('Transactions per second', [(None, 0)] + [(item, throughputs_dict[item]) for item in x_seq])
    fig.render_to_file(filename=os.path.join(dir, image_name))

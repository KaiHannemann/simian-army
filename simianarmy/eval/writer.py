import yaml
import datetime
from yaml.representer import Representer
import collections


def write_results(metric):
    f = open("results\\army_metrics_{}.yaml".format(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')), 'w+')
    yaml.add_representer(collections.defaultdict, Representer.represent_dict)
    yaml.dump(metric, f, default_flow_style=False)
    f.close()

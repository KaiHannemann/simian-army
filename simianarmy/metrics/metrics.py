import logging
logger = logging.getLogger(__name__)

# Metrics global dict
metrics = {}


# Initialize the metrics module
def reset():
    metrics['schedule'] = 0
    metrics['connection'] = 0
    metrics['shutdown'] = 0
    metrics['delay'] = 0
    metrics['rm_edge'] = []
    metrics['ch_schedule'] = []
    metrics['rm_vnf'] = []
    metrics['edge_delay'] = []
    metrics['data'] = []


def schedule(change):
    metrics['schedule'] += 1
    metrics['ch_schedule'].append(change)


def connection(change):
    metrics['connection'] += 1
    metrics['rm_edge'].append(change)


def shutdown(change):
    metrics['shutdown'] += 1
    metrics['rm_vnf'].append(change)


def delay(change):
    metrics['delay'] += 1
    metrics['edge_delay'].append(change)


def data(change):
    metrics['data'].append(change)
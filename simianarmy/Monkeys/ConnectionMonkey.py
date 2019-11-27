from simianarmy.Monkeys.Monkey import Monkey
import random
import logging
from simianarmy.metrics import metrics


log = logging.getLogger(__name__)


class ConnectionMonkey(Monkey):
    """"""
    kind = "Connection"

    def __init__(self, name, probability=None):
        """Set proper initial state"""
        super().__init__(name)
        if probability is None:
            self.probability = [(0.1, 150), (0.2, 300), (0.3, 500), (0.4, 1000), (0.5, 3000),
                                (0.6, 3700), (0.7, 65000), (0.8, 250000), (0.9, 700000), (1, 1300000)]
        else:
            self.probability = probability

    def __str__(self):
        """Make print of Monkey readable with stating kind and name of the instance"""
        return "Connection Monkey named: {}".format(self.name)

    def process_trigger(self, connection=None, *args, **kwargs):
        """Disconnects a the connection between two nodes
        needs a NetworkX Graph
        """
        network = kwargs['network']
        if network.edges:
            if connection is None:
                log.info("No connection provided, choosing random one")
                edges = []
                for edge in network.edges:
                    edges.append(edge)
                try:
                    edge = edges[random.randrange(1, len(edges), 1)]
                except ValueError:
                    log.info("No more edges found")
                    edge = None
                if edge is not None:
                    network.remove_edge(*edge)
            else:
                network.remove_edge(connection)
        else:
            log.info("No edges found")
        metrics.connection(edge)
        return network

    def get_timing(self, *args, **kwargs):
        prob = random.random()
        next_fail = 0
        for x, fail_delay in self.probability:
            if x >= prob:
                next_fail = fail_delay
                break
        return next_fail

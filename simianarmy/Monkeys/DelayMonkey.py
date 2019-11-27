from simianarmy.Monkeys.Monkey import Monkey
import random
import logging
from simianarmy.metrics import metrics

log = logging.getLogger(__name__)


class DelayMonkey(Monkey):
    """Increases delay between two nodes"""
    kind = "Delay"

    def __init__(self, name, max_delay=50, delay=100):
        """Set proper initial state"""
        super().__init__(name)
        self.max_delay = max_delay
        self.delay = delay

    def __str__(self):
        """Make print of Monkey readable with stating kind and name of the instance"""
        return "Delay Monkey named: {}".format(self.name)

    def process_trigger(self, link=None, delay=None, *args, **kwargs):
        """requires network as a NetworkX network object: DiGraph"""
        network = kwargs['network']
        edges = []
        if delay is None:
            log.info("No delay provided, choosing random one")
            delay = random.randrange(1, self.max_delay, 1)
        for edge in network.edges:
            edges.append(edge)
        if link is None:
            log.info("No link provided, choosing random one")
            link = random.choice(edges)
        network.edges[link]['delay'] = delay
        metrics.delay((link, delay))
        return network

    def get_timing(self, *args, **kwargs):
        return random.random() * self.delay

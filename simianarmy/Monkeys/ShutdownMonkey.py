from simianarmy.Monkeys.Monkey import Monkey
import random
import logging
from simianarmy.metrics import metrics

log = logging.getLogger(__name__)


class ShutdownMonkey(Monkey):
    """Shuts down a MFV instance"""

    kind = "Shutdown"

    def __init__(self, name, prob=0.00000661375):
        """Set proper initial state"""
        super().__init__(name)
        self.prob = prob

    def __str__(self):
        """Make print of Monkey readable with stating kind and name of the instance"""
        return "Shutdown Monkey named: {}".format(self.name)

    def process_trigger(self, node=None, sf=None, *args, **kwargs):
        """Shuts down a service function instance
        Needs network placement given in the from
        placement : dict
        {node1: [SF1, SF2],
        node2: [SF1]}
        optional:
        node : your node type
        sf : your service function type
        """
        placement = kwargs['placement']
        if node is None:
            log.info("No node provided, choosing random one")
            node = random.choice(list(placement.keys()))
        if placement[node]:
            if sf is None:
                log.info("No service function provided, choosing random one")
                sf = random.choice(placement[node])
            placement[node].remove(sf)
        metrics.shutdown((node, sf))
        return placement

    def get_timing(self, *args, **kwargs):
        next_fail = 0
        while True:
            next_fail += 1
            if random.random() < self.prob:
                break
        return next_fail

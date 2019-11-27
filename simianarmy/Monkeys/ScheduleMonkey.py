from simianarmy.Monkeys.Monkey import Monkey
import random
import numpy as np
import logging
from simianarmy.metrics import metrics

log = logging.getLogger(__name__)


class ScheduleMonkey(Monkey):
    """"""
    kind = "Schedule"

    def __init__(self, name, delay=10000):
        """Set proper initial state"""
        super().__init__(name)
        self.delay = delay

    def __str__(self):
        """Make print of Monkey readable with stating kind and name of the instance"""
        return "Schedule Monkey named: {}".format(self.name)

    def process_trigger(self, node=None, sfc=None, sf=None, *args, **kwargs):
        """Alters the schedule of Coord sim
        reschedules target_node probabilities of one node of one service function chain
        Needs schedule given in the from
        schedule = {
            node1: {
                sfc1: {
                    sf1: {
                        target_node1 : probability,
                        target_node2 : probability
                    },
                    sf2: {
                        target_node1 : probability
                    }
                },
                sfc2: {
                    sf1: {
                        target_node1 : probability
                    }
                }
            },
            node2: {
                sfc1: {
                    sf1: {
                        target_node1 : probability,
                        target_node2 : probability
                    },
                    sf2: {
                        target_node1 : probability
                    }
                }
            }
        }
        """
        schedule = kwargs['schedule']
        if not node:
            log.info("No node provided, choosing random one")
            node = random.choice(list(schedule.keys()))
        if not sfc:
            log.info("No service function chain provided, choosing random one")
            sfc = random.choice(list(schedule[node].keys()))
        if not sf:
            log.info("No service function provided, choosing random one")
            sf = random.choice(list(schedule[node][sfc].keys()))
        probabilities = np.random.dirichlet(np.ones(len(list(schedule[node][sfc][sf].items()))), size=1)
        probs = []
        for x in np.nditer(probabilities):
            probs.append(round(float(x), 1))
        for x, y in zip(list(schedule[node][sfc][sf].keys()), probs):
            schedule[node][sfc][sf][x] = y
        metrics.schedule((schedule[node][sfc][sf], node, sfc, sf, probs))
        return schedule

    def get_timing(self, *args, **kwargs):
        return random.random() * self.delay

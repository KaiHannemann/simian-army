from simianarmy.SimianArmy import SimianArmy
from simianarmy.config import Config
import random
from simianarmy.metrics import metrics
from simianarmy.eval import writer



class Adapter:
    """This is the Adapter to connect a given network with the frameworks Simian Army"""
    def __init__(self, config=Config(), army=SimianArmy()):
        """Set proper initial state"""
        self.config = config
        self.army = army
        self.army.assemble_army()
        self.last_event_time = 0
        self.metrics = metrics
        self.writer = writer
        metrics.reset()
        self.switcher = {
            "Shutdown": self.shutdown,
            "Schedule": self.schedule,
            "Delay": self.delay,
            "Connection": self.connection
        }

    def __str__(self):
        """"""
        return "Within this adapter the Simian Army contains: " + self.army.__str__()

    def one_time_failure(self, simulator, kind=None, name=None, *args, **kwargs):
        """"""
        kinds = set()
        for monkey in self.army.monkeys:
            kinds.add(monkey.kind)
        # If no kind is specified a random one is picked
        if kind is None:
            kind = random.choice(list(kinds))
        simulator.env.process(self.timeout(simulator, self.config.min_delay))
        simulator.env.process(self.kind_switcher(simulator, kind, name, *args, **kwargs))
        self.last_event_time = simulator.env.now

    def loop_failures(self, simulator, *args, **kwargs):
        kinds = set()
        for monkey in self.army.monkeys:
            kinds.add(monkey.kind)
        for k in kinds:
            simulator.env.process(self.loop_wrapper(self.switcher.get(k))(simulator, k, None, self, *args, **kwargs))

    def loop_failure(self, simulator, kind, name=None, *args, **kwargs):
        simulator.env.process(self.loop_wrapper(self.switcher.get(kind))(simulator, kind, name, self, *args, **kwargs))

    @staticmethod
    def loop_wrapper(func):
        def looped(simulator, kind, name, adapter, *args, **kwargs):
            while True:
                adapter.last_event_time = simulator.env.now
                yield simulator.env.process(adapter.timeout(simulator, adapter.config.min_delay))
                yield simulator.env.process(func(simulator, kind, name, *args, **kwargs))
        return looped

    def timeout(self, simulator, delay):
        if delay - (simulator.env.now - self.last_event_time) > 0:
            yield simulator.env.timeout(delay - (simulator.env.now - self.last_event_time))

    def kind_switcher(self, simulator, kind, name, *args, **kwargs):
        self.switcher.get(kind)(simulator, kind, name, *args, **kwargs)

    def shutdown(self, simulator, kind, name, *args, **kwargs):
        yield simulator.env.process(self.timeout(simulator, self.army.get_timing(kind)))
        simulator.params.sf_placement = self.sent_trigger(kind, name, placement=simulator.params.sf_placement,
                                                          *args, **kwargs)

    def schedule(self, simulator, kind, name, *args, **kwargs):
        yield simulator.env.process(self.timeout(simulator, self.army.get_timing(kind)))
        simulator.params.schedule = self.sent_trigger(kind, name, schedule=simulator.params.schedule,
                                                      *args, **kwargs)

    def delay(self, simulator, kind, name, *args, **kwargs):
        yield simulator.env.process(self.timeout(simulator, self.army.get_timing(kind)))
        simulator.params.network = self.sent_trigger(kind, name, network=simulator.params.network,
                                                     *args, **kwargs)

    def connection(self, simulator, kind, name, *args, **kwargs):
        yield simulator.env.process(self.timeout(simulator, self.army.get_timing(kind)))
        simulator.params.network = self.sent_trigger(kind, name, network=simulator.params.network, *args, **kwargs)

    def sent_trigger(self, kind, name=None, *args, **kwargs):
        """Enacts the specified type of Monkey"""
        return self.army.sent_trigger(kind, name, *args, **kwargs)

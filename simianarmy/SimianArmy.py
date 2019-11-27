from simianarmy.Monkeys.ShutdownMonkey import ShutdownMonkey
from simianarmy.Monkeys.DelayMonkey import DelayMonkey
from simianarmy.Monkeys.ConnectionMonkey import ConnectionMonkey
from simianarmy.Monkeys.ScheduleMonkey import ScheduleMonkey
import random
import logging

log = logging.getLogger(__name__)


class SimianArmy:
    """The Simian Army to collect and address Monkeys"""
    def __init__(self):
        """Set proper initial state"""
        self.monkeys = []

    def __str__(self):
        """Make print of Simian Army readable.
        List all monkeys in the army"""
        if self.monkeys:
            text = ""
            for mk in self.monkeys:
                text += "{m}, ".format(m=mk.__str__())
            return text[:-2]
        else:
            return "No Monkeys in the Army"

    def assemble_army(self):
        """Instantiates each available Monkey once"""
        self.add_monkey(ShutdownMonkey("SDM1"))
        self.add_monkey(DelayMonkey("DM1"))
        self.add_monkey(ConnectionMonkey("CM1"))
        self.add_monkey(ScheduleMonkey("SM1"))

    def add_monkey(self, mk):
        """Adds a monkey to the simian army"""
        self.monkeys.append(mk)

    def remove_monkey(self, kind, name=None):
        """Removes a specific monkey kind from the army"""
        for mk in self.monkeys:
            if mk.kind == kind:
                if name is not None:
                    if mk.name == name:
                        self.monkeys.remove(mk)
                else:
                    self.monkeys.remove(mk)

    def sent_trigger(self, kind=None, name=None, *args, **kwargs):
        if name is not None:
            for mk in self.monkeys:
                if mk.name == name:
                    return mk.process_trigger(*args, **kwargs)
            log.info("no monkey with that name found choosing random one")
            if kind is None:
                log.info("no kind provided, choosing random one")
                kinds = set()
                for monkey in self.monkeys:
                    kinds.add(monkey.kind)
                kind = random.choice(kinds)
            monkey = random.choice([monkey for monkey in self.monkeys if monkey.kind == kind])
            return monkey.process_trigger(*args, **kwargs)
        else:
            if kind is None:
                log.info("no kind provided, choosing random one")
                kinds = set()
                for monkey in self.monkeys:
                    kinds.add(monkey.kind)
                kind = random.choice(kinds)
            monkey = random.choice([monkey for monkey in self.monkeys if monkey.kind == kind])
            return monkey.process_trigger(*args, **kwargs)

    def get_timing(self, kind, name=None):
        if name is not None:
            for monkey in self.monkeys:
                if kind == monkey.kind and name == monkey.name:
                    return monkey.get_timing()
        else:
            for monkey in self.monkeys:
                if kind == monkey.kind:
                    return monkey.get_timing()

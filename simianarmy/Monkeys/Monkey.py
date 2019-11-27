class Monkey:
    """"""
    kind = "base monkey"

    def __init__(self, name):
        """Set proper initial state"""
        self.name = name

    def __str__(self):
        """Make print of Monkey readable with stating kind and name of the instance"""
        return "Monkey. In the base class"

    def process_trigger(self, *args, **kwargs):
        """Specify this for each monkey class.
        Defines what the Monkey actually does.
        Add arguments that can specify changeable objects within the fault injected network object.
        Returns the faulted network object"""
        raise NotImplementedError

    def get_timing(self, *args, **kwargs):
        """Specify this for each monkey class.
        Returns the time between faults"""
        raise NotImplementedError

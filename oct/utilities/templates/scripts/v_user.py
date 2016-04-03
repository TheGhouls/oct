from oct_turrets.base import BaseTransaction
from oct_turrets.tools import CustomTimer
import random
import time


class Transaction(BaseTransaction):
    def __init__(self, config):
        super(Transaction, self).__init__(config)

    def setup(self):
        """Setup data or objects here
        """
        pass

    def run(self):
        r = random.uniform(1, 2)
        time.sleep(r)
        with CustomTimer(self, 'a timer'):
            time.sleep(r)

    def tear_down(self):
        """Clear cache or reset objects, etc. Anything that must be done after
        the run method and before its next execution
        """
        pass


if __name__ == '__main__':
    trans = Transaction(None)
    trans.run()
    print(trans.custom_timers)

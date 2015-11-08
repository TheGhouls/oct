from oct_turrets.base import BaseTransaction
import random
import time


class Transaction(BaseTransaction):
    def __init__(self):
        pass

    def setup(self):
        """Setup data or objects here
        """
        pass

    def run(self):
        r = random.uniform(1, 2)
        time.sleep(r)
        self.custom_timers['Example_Timer'] = r

    def tear_down(self):
        """Clear cache or reset objects, etc. Anything that must be done after
        the run method and before its next execution
        """
        pass


if __name__ == '__main__':
    trans = Transaction()
    trans.run()
    print(trans.custom_timers)

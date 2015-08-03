from oct.core.generic import GenericTransaction
import random
import time
import os


CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../')


class Transaction(GenericTransaction):
    def __init__(self):
        GenericTransaction.__init__(self, CONFIG_PATH)

    def run(self):
        r = random.uniform(1, 2)
        time.sleep(r)
        self.custom_timers['Example_Timer'] = r


if __name__ == '__main__':
    trans = Transaction()
    trans.run()
    print(trans.custom_timers)

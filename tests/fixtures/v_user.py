from oct_turrets.base import BaseTransaction
import time


class Transaction(BaseTransaction):
    def __init__(self):
        pass

    def run(self):
        start = time.time()
        time.sleep(0.2)
        self.custom_timers['Example_Timer'] = time.time() - start

from oct_turrets.base import BaseTransaction
import time


class Transaction(BaseTransaction):
    def run(self):
        start = time.time()
        time.sleep(0.2)
        self.custom_timers['Example_Timer'] = time.time() - start

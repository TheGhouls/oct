from oct_turrets.base import BaseTransaction
import random
import time


class Transaction(BaseTransaction):
    def __init__(self):
        pass

    def run(self):
        r = random.uniform(1, 2)
        time.sleep(r)
        raise Exception("This failed")

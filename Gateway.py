import time

from Amot import Amot

class Gateway:

    #
    def __init__(self):
        super().__init__()

    #
    def setup(self):
        pass
        
    #
    def loop(self):   
        print("Listening...")
        
        Amot.starter().run(peri_nodes)

        # do something
        pass


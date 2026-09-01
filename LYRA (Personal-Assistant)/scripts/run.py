import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import multiprocessing
import subprocess

# To run LYRA
def startLYRA():
        # Code for process 1
        print("Process 1 is running.")
        from lyra.core.main import start
        start()

# To run hotword
def listenHotword():
        # Code for process 2
        print("Process 2 is running.")
        from lyra.modules.features import hotword
        hotword()


    # Start both processes
if __name__ == '__main__':
        p1 = multiprocessing.Process(target=startLYRA)
        p2 = multiprocessing.Process(target=listenHotword)
        p1.start()
        p2.start()
        p1.join()

        if p2.is_alive():
            p2.terminate()
            p2.join()

        print("system stop")
import threading
import time

import psutil


class BackgroundServerMonitor:
    def __init__(self):
        self.monitor_server_stats = False
        self.start()
        self.memory = None
        self.cpu_percent = None

    def stop(self):
        self.monitor_server_stats = False
        self.thread.join()

    def start(self):
        self.monitor_server_stats = True
        self.thread = threading.Thread(target=self.grab_server_stats)
        self.thread.start()

    def grab_server_stats(self):
        mem = psutil.virtual_memory().percent
        cpu = psutil.cpu_percent()
        index = 1
        while self.monitor_server_stats:
            index += 1
            mem = ((mem * (index-1)) + psutil.virtual_memory().percent) / index
            cpu = ((cpu * (index-1)) + psutil.cpu_percent()) / index
            time.sleep(1)

        self.memory = mem
        self.cpu_percent = cpu
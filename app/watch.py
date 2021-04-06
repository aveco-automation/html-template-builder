import sys
import time

from nxtools import *

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler


class WatchHandler():
    def __init__(self, callback):
        self.callback = callback
        self.queue = set()
        self.last_event = 0

    def dispatch(self, event):
        self.queue.add(event.src_path)
        self.last_event = time.time()

    def process(self):
        if not self.queue:
            return
        if time.time() - self.last_event > 0.05:
            self.callback(list(self.queue))
            self.queue = set()



class Watch():
    def __init__(self, path, callback):
        self.handler = WatchHandler(callback)
        self.observer = Observer()
        self.observer.schedule(self.handler, path, recursive=True)
        self.should_run = False
        self.running = False


    def start(self):
        self.observer.start()
        self.should_run = True
        self.running = True

        try:
            while self.should_run:
                time.sleep(.01)
                self.handler.process()
        except Exception:
            log_traceback()


    def stop(self):
        logging.info("Stopping watch")
        self.should_run = False

        if self.running:
            self.observer.stop()
            self.observer.join()
            self.running = False
        logging.info("Stopped")

    def __del__(self):
        self.stop()

"""Directory watcher.

Wath source directory and rebuild the html files
when a source file changes.
"""

import time

from nxtools import logging, log_traceback
from watchdog.observers import Observer


class WatchHandler():
    """Watch event handler."""

    def __init__(self, callback):
        """Watch handler constructor."""
        self.callback = callback
        self.queue = set()
        self.last_event = 0

    def dispatch(self, event):
        """Dispatch event."""
        self.queue.add(event.src_path)
        self.last_event = time.time()

    def process(self):
        """Process enqueued events."""
        if not self.queue:
            return
        if time.time() - self.last_event > 0.05:
            self.callback(list(self.queue))
            self.queue = set()


class Watch():
    """Directory watcher."""

    def __init__(self, path, callback):
        """Watch constructor."""
        self.handler = WatchHandler(callback)
        self.observer = Observer()
        self.observer.schedule(self.handler, path, recursive=True)
        self.should_run = False
        self.running = False

    def start(self):
        """Start watching."""
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
        """Stop watching."""
        logging.info("Stopping watch")
        self.should_run = False

        if self.running:
            self.observer.stop()
            self.observer.join()
            self.running = False
        logging.info("Stopped")

    def __del__(self):
        """Watch destructor."""
        self.stop()

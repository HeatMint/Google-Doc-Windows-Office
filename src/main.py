#!/usr/bin/python
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
path = '../test_location'

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        print(event.event_type, event.src_path)
        file_name = event.src_path[len(path)+1:]

    def on_moved(self, event):
        print(event.event_type, event.src_path,event.dest_path)
        file_name = event.dest_path[len(path) + 1:]

    def on_any_event(self, event):
        print(event.event_type, event.src_path)


if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
import time
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from plyer import notification

class Watcher:
    # Directory to monitor the status.json file
    FILE_TO_WATCH = r"C:\Users\Singh\Desktop\DDAS\status.json"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler(self.FILE_TO_WATCH)
        # Monitoring the parent directory of status.json
        self.observer.schedule(event_handler, path=self.get_directory_to_watch(), recursive=False)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

    def get_directory_to_watch(self):
        # Returns the directory path where status.json is located
        return self.FILE_TO_WATCH.rsplit('\\', 1)[0]

class Handler(FileSystemEventHandler):
    def __init__(self, file_to_watch):
        self.file_to_watch = file_to_watch

    def on_modified(self, event):
        if event.src_path == self.file_to_watch:
            self.process_event()

    def process_event(self):
        # Reads the status.json file and triggers a desktop notification
        with open(self.file_to_watch, 'r') as f:
            data = json.load(f)
            message = data.get("lastMessage", "No message found.")
            notification.notify(
                title='File Upload Status',
                message=message,
                timeout=10
            )

if __name__ == '__main__':
    w = Watcher()
    w.run()

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.events import PatternMatchingEventHandler
import os
import time
import sys
import time
import logging
from obswebsocket import requests, events
import obswebsocket.requests


logging.basicConfig(level=logging.INFO)
sys.path.append('../')

def on_event(message):
    print("Got message: {}".format(message))

def on_switch(message):
    print("You changed the scene to {}".format(message.getSceneName()))

client = obswebsocket.obsws("localhost", 4444, "secret")
client.connect()
client.call(obswebsocket.requests.GetVersion()).getObsWebsocketVersion()
client.register(on_event)
client.register(on_switch, events.SwitchScenes)


def scene():
    try:
        client.call(requests.SetCurrentScene('Scene'))
        time.sleep(2)
    except KeyboardInterrupt:
        pass

def scene2():
    try:
        client.call(requests.SetCurrentScene('Scene2'))
        time.sleep(2)
    except KeyboardInterrupt:
        pass

class ChangeHandler(PatternMatchingEventHandler):
    patterns = ["*.txt"]

    def process(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """

        print ("Received modified event - %s." % event.src_path)



    def on_any_event(self, event):
        scene2()
        time.sleep(6)
        scene()
        self.process(event)


dirname = os.path.dirname(__file__)

if __name__ == '__main__':
    observer = Observer()
    observer.schedule(ChangeHandler(), path=dirname, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()
    observer.join()
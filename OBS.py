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
        client.call(requests.SetCurrentScene('scene'))
        time.sleep(2)
    except KeyboardInterrupt:
        pass

def scene2():
    try:
        client.call(requests.SetCurrentScene('scene2'))
        time.sleep(2)
    except KeyboardInterrupt:
        pass




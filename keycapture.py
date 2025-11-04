# This file will read and process keyboard inputs
from pynput import keyboard
import time

def on_action(data, key: keyboard.KeyCode | keyboard.Key| None):
    data.add(key)
    return

# Colect key presses over a timespan
def readTimespan(timeSpanMSL: int):
    keyPressSet = set()
    keyReleaseSet = set()
    listener: keyboard.Listener = keyboard.Listener(
        on_press=lambda key:on_action(keyPressSet, key),
        on_release=lambda key:on_action(keyReleaseSet, key)
    )
    listener.start()
    time.sleep(timeSpanMSL/ 1000)
    listener.stop()
    return keyPressSet, keyReleaseSet

        

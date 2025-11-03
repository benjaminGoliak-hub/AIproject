from pynput import keyboard
import time

def on_action(data, key: keyboard.KeyCode | keyboard.Key| None):
    data.add(key)
    return

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
    print('Pressed:', keyPressSet)
    print('Released:', keyReleaseSet)
    

readTimespan(5000)
        

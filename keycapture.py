from pynput import keyboard
import time

def on_press(key):
    print('Press')
    return

def on_release(key):
    return

def readTimespan(timeSpanMSL: int):
    listener: keyboard.Listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    listener.start()
    time.sleep(timeSpanMSL/ 1000)
    listener.stop()
    
    



readTimespan(1000)
        

# Main loop which controls the program flow etc

from os import abort
from pynput import keyboard
import time

global SAMPLE_TIME
global SAMPLE_COUNT
global KEYS
KEYS = (keyboard.KeyCode.from_char('w'), 
    keyboard.KeyCode.from_char('a'),
    keyboard.KeyCode.from_char('s'),
    keyboard.KeyCode.from_char('d'))
SAMPLE_TIME = int(1000/15)
SAMPLE_COUNT = 60

def _on_action(data, key: keyboard.KeyCode | keyboard.Key| None):
    data.add(key)

while True:
    step_inputs = set()
    actionListener = keyboard.Listener(
        on_press=lambda key:_on_action(step_inputs, key))
    actionListener.start()
    time.sleep(SAMPLE_TIME/1000)
    print(step_inputs)
    if keyboard.Key.esc in step_inputs:
        exit()
    



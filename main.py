# Main loop which controls the program flow etc

import multiprocessing
from multiprocessing import process
from os import abort
from pynput import keyboard
from globals import SAMPLE_TIME, SAMPLE_COUNT
import datamanager
import time
import network




def _on_action(data, key: keyboard.KeyCode | keyboard.Key| None):
    data.add(key)
    
while True:
    step_inputs = set()
    # Get user commands
    actionListener = keyboard.Listener(
        on_press=lambda key:_on_action(step_inputs, key))
    actionListener.start()
    time.sleep(SAMPLE_TIME/1000)

    
    if keyboard.Key.enter in step_inputs:
        States, Actions = datamanager.collectPairs(SAMPLE_TIME, SAMPLE_COUNT)
        
    if keyboard.KeyCode.from_char('\\') in step_inputs:
        pass
    # Exit
    if keyboard.Key.esc in step_inputs:
        exit()

    # Capture screen info. Only do this once
    



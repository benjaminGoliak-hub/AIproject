# Main loop which controls the program flow etc

import multiprocessing
from multiprocessing import process
from os import abort
from pynput import keyboard
from globals import SAMPLE_TIME, SAMPLE_COUNT
import datamanager
import time




def _on_action(data, key: keyboard.KeyCode | keyboard.Key| None):
    data.add(key)
    
while True:
    step_inputs = set()
    # Get user commands
    actionListener = keyboard.Listener(
        on_press=lambda key:_on_action(step_inputs, key))
    actionListener.start()
    time.sleep(SAMPLE_TIME/1000)
    print(step_inputs)

    
    if keyboard.Key.enter in step_inputs:
        States, Actions = datamanager.collectPairs(SAMPLE_TIME, SAMPLE_COUNT)
        
    
    # Exit
    if keyboard.Key.esc in step_inputs:
        print(Actions)
        exit()

    # Capture screen info. Only do this once
    



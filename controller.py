import torch
import mss
import cv2
import numpy as np
from pynput import keyboard
from torch import nn
from globals import PROGRAM_DTYPE, CAPTURED_SCALE, CAPTURED_KEYS
    
def model_control(model: nn.Module, inputDevice: keyboard.Controller):
    screen = None
    pressedStates = {key: False for key in CAPTURED_KEYS}

    def press(actions: dict[keyboard.Key | keyboard.KeyCode, bool]):
        for key in actions.keys():
            if actions[key] != pressedStates[key]:
                if actions[key] == 1:
                    inputDevice.press(key)
                else:
                    inputDevice.release(key)
                pressedStates[key] = actions[key]
    
    # Gets picture
    with mss.mss() as sct:
        monitor = sct.monitors[1] 
        screenshot = np.array(sct.grab(monitor))
        grey = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)
        scaled = cv2.resize(grey, CAPTURED_SCALE).astype(PROGRAM_DTYPE)
        screen = scaled / 255.0
    
    
    

    
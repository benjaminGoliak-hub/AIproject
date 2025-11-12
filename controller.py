import torch
import mss
import cv2
import numpy as np
import time
import threading
from pynput import keyboard
from torch import nn
from globals import DEVICE, PROGRAM_TTYPE, PROGRAM_DTYPE, CAPTURED_SCALE, CAPTURED_KEYS, SAMPLE_RATE

# Controlls the keyboard
def model_control(model: nn.Module, inputDevice: keyboard.Controller):
    screen = None
    pressedStates = {key: False for key in CAPTURED_KEYS}
    stop_event = threading.Event()

    def press(key: keyboard.Key | keyboard.KeyCode, state: bool):
        if state != pressedStates[key]:
            if state:
                inputDevice.press(key)
            else:
                inputDevice.release(key)
            pressedStates[key] = state

    # Sets up a listener to wait for escape to be pressed
    def onEscape(key) -> bool | None:
        if key == keyboard.Key.esc:
            print('[INFO] escape!')
            stop_event.set()
            return False

    escapeListener = keyboard.Listener(
        on_press=onEscape # My IDE hates this but it works
    )

    escapeListener.start()

    try:
        with mss.mss() as sct:
            while not stop_event.is_set():
                # Gets picture
                monitor = sct.monitors[1] 
                screenshot = np.array(sct.grab(monitor))
                grey = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)
                scaled = cv2.resize(grey, CAPTURED_SCALE).astype(PROGRAM_DTYPE)
                screen = torch.tensor(scaled / 255.0, dtype=PROGRAM_TTYPE).unsqueeze(0).unsqueeze(0).to(DEVICE)
                
                with torch.no_grad():
                    actions = model(screen).cpu().numpy()

                for i, key in enumerate(CAPTURED_KEYS):
                    press(key, actions[0][i] > 0.5)
                
                time.sleep(SAMPLE_RATE)
        
        escapeListener.join()

    finally:
        for i, key in enumerate(CAPTURED_KEYS):
            press(key, False)
    
    

            

    
    
    

    
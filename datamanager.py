# This file will be responsible for compiling datasamples and controlling how they
# Are gathered 
# Decided to restructure this into a class type to make life easier
# Also moving to files to save data

from pynput import keyboard
from threading import Lock
from globals import PROGRAM_DTYPE, SAMPLE_RATE, SNIPIT_DIR
import time
import mss
import pickle
import os
import numpy as np
import cv2

class DataManager:
    # Init function
    def __init__(self, recordingScale: tuple[int, int], recordingKeys: list[keyboard.Key | keyboard.KeyCode]) -> None:
        self.recordingScale = recordingScale
        self.recordingKeys = recordingKeys

        self.isRecording = False
        self.isRecording_LOCK = Lock()

        self.keyStates = {key: False for key in self.recordingKeys}
        self.keyStates_LOCK = Lock()
        
        self.recordedData = []
        self.recordedData_LOCK = Lock()
    
    # Gets and processes screenshot
    def _grabscreen(self):
        with mss.mss() as sct:
            monitor = sct.monitors[1] 
            screenshot = np.array(sct.grab(monitor))
            grey = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)
            scaled = cv2.resize(grey, self.recordingScale).astype(PROGRAM_DTYPE)
            return scaled / 255.0
    
    # On action function for key reading
    # Use try because it caused errors before sometimes
    def _onAction(self, toggle: bool, key: keyboard.Key | keyboard.KeyCode | None) -> None:
        try:
            if key in self.recordingKeys:
                assert(key is not None) # My language checker makes me unwrap this
                self.keyStates_LOCK.acquire()
                self.keyStates[key] = toggle
                self.keyStates_LOCK.release()
        except:
            pass
    
    # Start recording
    # The reason it is a class now so that it has state
    def record(self):
        print('[INFO] Key recording requested')

        # Start the state of this
        self.isRecording_LOCK.acquire()
        assert(not self.isRecording) # Protect from double calls because this may run async
        self.isRecording = True
        self.isRecording_LOCK.release()

        # Make and run the listener to hear inputs
        keyListener = keyboard.Listener(
            on_press=lambda key:self._onAction(True, key),
            on_release=lambda key:self._onAction(False, key)
        )
        keyListener.start()

        print('[INFO] Key recording has started')

        # Loop untill another thread changes the isRecording state
        self.recordedData = []
        while self.isRecording:
            # Get the screenshot
            frame = self._grabscreen()

            # Save the keys
            self.keyStates_LOCK.acquire()
            action = np.array([int(self.keyStates[key]) for key in self.recordingKeys]).astype(PROGRAM_DTYPE)
            self.keyStates_LOCK.release()

            self.recordedData_LOCK.acquire()
            self.recordedData.append((frame, action))
            self.recordedData_LOCK.release()

            # Sleep
            time.sleep(SAMPLE_RATE)
        
        keyListener.stop()
        print(f'[INFO] Key recording has stopped. Recorded {len(self.recordedData)} samples')
    
    # Stops the recording
    def stop(self) -> None:
        assert(self.isRecording)
        self.isRecording = False

    # Save using the pickle
    def saveData(self, fileName: str) -> None:
        # Makes the directory to save data to
        os.makedirs(SNIPIT_DIR, exist_ok=True) 
        pathName = os.path.join(SNIPIT_DIR, fileName)

        # Save the output
        self.recordedData_LOCK.acquire()
        with open(pathName, 'wb') as dataFile:
            pickle.dump(self.recordedData, dataFile)
        self.recordedData_LOCK.release()

        print(f'[INFO] Saved recording to {pathName}')
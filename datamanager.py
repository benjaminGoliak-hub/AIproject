# This file will be responsible for compiling datasamples and controlling how they
# Are gathered 
# Decided to restructure this into a class type to make life easier
# Also moving to files to save data

from pynput import keyboard
from threading import Lock
from globals import PROGRAM_DTYPE, SAMPLE_RATE
import time
import mss
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
        while self.isRecording:
            # Get the screenshot
            frame = self._grabscreen()

            # Save the keys
            self.keyStates_LOCK.acquire()
            action = np.array(int(self.keyStates[key]) for key in self.recordingKeys)
            self.keyStates_LOCK.release()

            self.recordedData.append((frame, action))

            # Sleep
            time.sleep(SAMPLE_RATE)
        
        keyListener.stop()
        print(f'[INFO] Key recording has stopped. Recorded {len(self.recordedData)} samples')
    
    # Stops the recording
    def stop(self) -> None:
        assert(self.isRecording)
        self.isRecording = False


        

    

    

        







# # get screenshot
# def _grabscreen():
#     with mss.mss() as sct:
#     # Get raw pixels from the entire screen
#         monitor = sct.monitors[1]  # Use sct.monitors[0] for all monitors
#         screenshot = sct.grab(monitor)
#         return np.array(screenshot)
        
# # Pre-process screenshot
# def _preprocess(array: np.ndarray):
#     grey = cv2.cvtColor(array, cv2.COLOR_RGB2GRAY)
#     scaled = cv2.resize(grey, SCALE)
#     scaled = scaled.astype(FLOATTYPE)
#     scaled /= 256.0
#     return scaled

# def _getScreenData() -> np.ndarray:
#     return _preprocess(_grabscreen())

# def _on_action(data, key: keyboard.KeyCode | keyboard.Key| None):
#     data.add(key)

# # Colect key presses over a timespan
# def _readTimespan(timeSpanMSL: int):
#     keyPressSet = set()
#     keyReleaseSet = set()
#     listener: keyboard.Listener = keyboard.Listener(
#         on_press=lambda key:_on_action(keyPressSet, key),
#         on_release=lambda key:_on_action(keyReleaseSet, key)
#     )
#     listener.start()
#     time.sleep(timeSpanMSL/ 1000)
#     listener.stop()
#     return keyPressSet, keyReleaseSet

# def _translateKeys(keyPressSet: set, keyReleaseSet: set) -> np.ndarray:
#     keyArray = np.zeros(2 * len(KEYS), FLOATTYPE)
#     for i in range(len(KEYS)):
#         if KEYS[i] in keyPressSet:
#             keyArray[i] = 1.0
#         if KEYS[i] in keyReleaseSet:
#             keyArray[i + len(KEYS)] = 1.0
#     return keyArray

# def _getKeyData(timespan: int):
#     keysPressed, keysReleased = _readTimespan(timespan)
#     return _translateKeys(keysPressed, keysReleased)

# # Collect a set of pairs to use
# def collectPairs(timespan: int, count: int):
#     stateSet = np.empty(shape=(count, SCALE[0] * SCALE[1]), dtype=FLOATTYPE)
#     actionSet = np.empty(shape=(count, 2 * len(KEYS)), dtype=FLOATTYPE)
#     for i in range(count):
#         stateData = _getScreenData()
#         stateSet[i] = stateData.ravel()
#         actionData = _getKeyData(timespan)
#         actionSet[i] = actionData
#     return stateSet, actionSet



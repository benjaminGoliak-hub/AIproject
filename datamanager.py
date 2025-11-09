# This file will be responsible for compiling datasamples and controlling how they
# Are gathered

from pynput import keyboard
from main import KEYS as KEYS
import time
import mss
import numpy as np
import cv2

global SCALE 
SCALE = (128, 128)
FLOATTYPE = np.float16

# get screenshot
def _grabscreen():
    with mss.mss() as sct:
    # Get raw pixels from the entire screen
        monitor = sct.monitors[1]  # Use sct.monitors[0] for all monitors
        screenshot = sct.grab(monitor)
        return np.array(screenshot)
        
# Pre-process screenshot
def _preprocess(array: np.ndarray):
    grey = cv2.cvtColor(array, cv2.COLOR_RGB2GRAY)
    scaled = cv2.resize(grey, SCALE)
    scaled = scaled.astype(FLOATTYPE)
    scaled /= 256.0
    return scaled

def _getScreenData() -> np.ndarray:
    return _preprocess(_grabscreen())

def _on_action(data, key: keyboard.KeyCode | keyboard.Key| None):
    data.add(key)

# Colect key presses over a timespan
def _readTimespan(timeSpanMSL: int):
    keyPressSet = set()
    keyReleaseSet = set()
    listener: keyboard.Listener = keyboard.Listener(
        on_press=lambda key:_on_action(keyPressSet, key),
        on_release=lambda key:_on_action(keyReleaseSet, key)
    )
    listener.start()
    time.sleep(timeSpanMSL/ 1000)
    listener.stop()
    return keyPressSet, keyReleaseSet

def _translateKeys(keyPressSet: set, keyReleaseSet: set) -> np.ndarray:
    keyArray = np.zeros(2 * len(KEYS), FLOATTYPE)
    for i in range(len(KEYS)):
        if KEYS[i] in keyPressSet:
            keyArray[i] = 1.0
        if KEYS[i] in keyReleaseSet:
            keyArray[i + len(KEYS)] = 1.0
    return keyArray

def _getKeyData(timespan: int):
    keysPressed, keysReleased = _readTimespan(timespan)
    return _translateKeys(keysPressed, keysReleased)

# Collect a set of pairs to use
def collectPairs(timespan: int, count: int):
    stateSet = np.empty(shape=(count, SCALE[0] * SCALE[1]), dtype=FLOATTYPE)
    actionSet = np.empty(shape=(count, 2 * len(KEYS)), dtype=FLOATTYPE)
    for i in range(count):
        stateData = _getScreenData()
        stateSet[i] = stateData.ravel()
        actionData = _getKeyData(timespan)
        actionSet[i] = actionData
    return stateSet, actionSet



# This file will be responsible for code about gathering and processing screen shots
import mss
import mss.tools
from PIL import Image
import numpy as np
import cv2
from numpy.typing import NDArray

# get screenshot
def _grabscreen():
    with mss.mss() as sct:
    # Get raw pixels from the entire screen
        monitor = sct.monitors[1]  # Use sct.monitors[0] for all monitors
        screenshot = sct.grab(monitor)
        return np.array(screenshot)
        
# Pre-process screenshot
def _preprocess(array: np.ndarray):
    SCALE = (128, 128)
    grey = cv2.cvtColor(array, cv2.COLOR_RGB2GRAY)
    return cv2.resize(grey, SCALE)
    
    # array = array + 80
    # array = cv2.cvtColor(array, cv2.COLOR_RGB2HLS)
    # lum = cv2.equalizeHist(cv2.extractChannel(array, 2))
    # array = cv2.insertChannel(lum, array, 2)
    # array = cv2.cvtColor(array, cv2.COLOR_HLS2RGB)
    # return cv2.resize(array, (16*50,9*50))

def getScreenData() -> np.ndarray:
    return _preprocess(_grabscreen())






from io import FileIO
from pynput import keyboard
import numpy as np

# Set of keys we care about listening to and recording
global CAPTURED_KEYS

def _fromChar(keychr: str) -> keyboard.KeyCode:
    return keyboard.KeyCode.from_char(keychr)

CAPTURED_KEYS = (
    _fromChar('w'),
    _fromChar('a'),
    _fromChar('s'),
    _fromChar('d'))

# Data type to save info as
global PROGRAM_DTYPE

PROGRAM_DTYPE = np.float32

# Time between each input logging (in MS)
global SAMPLE_RATE

SAMPLE_RATE = 1000 / 20

# Directory for saved snipits
global SNIPIT_DIR
SNIPIT_DIR = 'saves'







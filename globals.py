from io import FileIO
from cv2 import scaleAdd
from pynput import keyboard
import numpy as np
import torch

# Set of keys we care about listening to and recording
global CAPTURED_KEYS

def _fromChar(keychr: str) -> keyboard.KeyCode:
    return keyboard.KeyCode.from_char(keychr)

CAPTURED_KEYS: list[keyboard.Key | keyboard.KeyCode] = [
    _fromChar('w'),
    _fromChar('a'),
    _fromChar('s'),
    _fromChar('d')]

global CAPTURED_SCALE
CAPTURED_SCALE = (128,128)

# Data type to save info as
global PROGRAM_DTYPE, PROGRAM_TTYPE

# These need to be the same type
PROGRAM_DTYPE = np.float32
PROGRAM_TTYPE = torch.float32


# Time between each input logging (in MS)
global SAMPLE_RATE

SAMPLE_RATE = 1 / 20

# Directory for saved snipits
global SNIPIT_DIR
SNIPIT_DIR = 'saves'

# Device for the training
global DEVICE
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

global STACK_FRAMES
STACK_FRAMES = [0, 1, 4, 8]






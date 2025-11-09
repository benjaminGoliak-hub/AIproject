from pynput import keyboard

global SAMPLE_TIME
global SAMPLE_COUNT
global KEYS
KEYS = (keyboard.KeyCode.from_char('w'), 
    keyboard.KeyCode.from_char('a'),
    keyboard.KeyCode.from_char('s'),
    keyboard.KeyCode.from_char('d'))
SAMPLE_TIME = int(1000/15)
SAMPLE_COUNT = 60
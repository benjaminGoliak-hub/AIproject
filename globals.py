from pynput import keyboard


# Set of keys we care about listening to and recording
global CAPTURED_KEYS

def _fromChar(keychr: str) -> keyboard.KeyCode:
    return keyboard.KeyCode.from_char(keychr)

CAPTURED_KEYS = (
    _fromChar('w'),
    _fromChar('a'),
    _fromChar('s'),
    _fromChar('d'))






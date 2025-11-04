# This file will be responsible for compiling datasamples and controlling how they
# Are gathered
import keycapture
import screengrab
import threading

# Captures a pair of action/state without blocking
def capturepair(timespan: int):
    key_thread = threading.Thread(target=keycapture.readTimespan, args=[timespan])
    key_thread.start()
    img = screengrab.getScreenData()
    key_thread.join()
import mss
import mss.tools
from PIL import Image

with mss.mss() as sct:
    # Get raw pixels from the entire screen
    monitor = sct.monitors[1]  # Use sct.monitors[0] for all monitors
    screenshot = sct.grab(monitor)

    # Save to a file
    mss.tools.to_png(screenshot.rgb, screenshot.size, output="mss_screenshot.png")

    # Alternatively, convert to a PIL Image object
    # img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")

print("Screenshot saved as mss_screenshot.png")

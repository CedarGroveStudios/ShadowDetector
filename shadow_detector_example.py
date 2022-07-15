# shadow_detector_example.py

import board
import time
from shadow_detector import ShadowDetector

# Instantiate detector class and establish background level
gesture = ShadowDetector(pin=board.LIGHT)

while True:
    if gesture.detect():
        print(f"SHADOW DETECTED")
        while gesture.detect():
            # Wait until the shadow is gone
            time.sleep(1)
        # Rebaseline the background level
        gesture.refresh_background()
        print(f"background: {gesture.background:6.0f}")

# shadow_detector_example.py

import board
import time
from shadow_detector import ShadowDetector

gesture = ShadowDetector(pin=board.LIGHT)

while True:
    if gesture.detect():
        print(f"SHADOW DETECTED")
        while gesture.detect():
            time.sleep(1)
        gesture.refresh_background()

# ShadowDetector

A CircuitPython class to detect a shadow cast over an analog light sensor such as the ALS-PT19 phototransistor used in the Adafruit PyPortal, PyGamer, PyBadge, CircuitPlayground Express, CircuitPlayground Bluefruit, and the ALS-PT19 breakout board. Incorporates an optional low-pass filter to reduce sensitivity to flickering light levels greater than 25 Hz.

    Useful as a simple gesture detector.

The ShadowDetector has only been tested on the PyPortal so far, but should be able to function reliably on other microcontrollers. The automatic sampling mode will test the microcontroller's analog acquisition latency and adjust the internal low-pass filter's sample size to maintain the 25 Hz cutoff frequency.

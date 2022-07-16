# ShadowDetector

A CircuitPython class to detect a shadow cast over an analog light sensor such as the ALS-PT19 phototransistor used in the Adafruit PyPortal, PyGamer, PyBadge, CircuitPlayground Express, CircuitPlayground Bluefruit, and the ALS-PT19 breakout board. Incorporates an optional low-pass filter to reduce sensitivity to flickering light levels which may be caused by power line frequency or light dimmer PWM pass through..

    Useful as a simple gesture detector.

The ShadowDetector has only been tested on the PyPortal so far, but should be able to function reliably on other microcontrollers. The automatic sampling mode will test the microcontroller's analog acquisition latency and adjust the internal low-pass filter's sample size to maintain the 25 Hz cutoff frequency.

![Light sensor signal low-pass filter comparison](https://github.com/CedarGroveStudios/ShadowDetector/blob/main/docs/FIR_boxcar_filter_pyportal.png)

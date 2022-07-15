# Shadow Detector
# Copyright 2022 by JG for Cedar Grove Maker Studios
#
# gesture_detector.py 2022-07-14 v1.0714

import board
import time
from analogio import AnalogIn

class ShadowDetector():
    """A CircuitPython class to detect a shadow cast over an analog
    light sensor such as the ALS-PT19 phototransistor used in the Adafruit
    PyPortal, PyGamer, PyBadge, CircuitPlayground Express, CircuitPlayground
    Bluefruit, and the ALS-PT19 breakout board. Useful as a simple gesture
    detector."""

    def __init__(self, pin, threshold=0.9, samples=2000, auto=False, decay=0.01):
        """Class initializer. Measure the initial background light level and
        automatically select the optimal number of samples for the low-pass
        filter if auto = True.
        The decay factor value is the fraction of influence the foreground has
        on adjusting the previously measured background level; 0.01 is a weight
        of 1 part foreground for 99 parts background. Decay defaults to 0.01;
        range is 0.0 to 1.0"""

        self._light_sensor = AnalogIn(pin)
        self._brightness_threshold = threshold
        self._samples = samples
        self._decay = max(min(decay, 1.0), 0.0)

        if auto:
            """Calculate the number of samples needed to achieve a target
            per-sample delay of 135 usec (0.000135 sec). Creates an n-order
            finite impulse response (FIR) moving-average (boxcar) low-pass 
            filter."""
            print("automatic samples calculation")
            test_samples = [2000, 8000]  # Typical min and max samples values
            test_delays = []
            for i, self._samples in enumerate(test_samples):
                t0 = time.monotonic()
                self.refresh_background()
                test_delays.append((time.monotonic() - t0) / self._samples)
            # Create slope-intercept formula based on test values; y = mx + b
            slope = ((test_samples[1] - test_samples[0]) / (test_delays[1] - test_delays[0]))
            intercept = test_samples[1] - (slope * test_delays[1])
            self._samples = int((slope * 0.000135) + intercept)
        else:
            # Use default or provided samples value
            print("default samples calculation")
            self._samples = samples
        print(f"samples: {self._samples:6.0f}")


    def _read(self):
        """Read sensor and filter measurement using discrete time FIR filter of
        order = self._samples, sample delay = self._sample_delay."""
        measurement = 0
        for i in range(self._samples):
            measurement = measurement + (self._light_sensor.value / self._samples)
        return measurement


    def _get_foreground(self):
        """Read foreground sensor value. Background level is adjusted slightly
        each time the foreground level is read per the decay setting."""
        self._foreground = self._read()
        self._background = ((1.0 - self._decay) * self._background) + (self._decay * self._foreground)
        return


    def refresh_background(self):
        """Read background sensor value."""
        print("Refresh light sensor background measurement")
        self._background = self._read()
        return


    def detect(self):
        """Compare foreground to background light levels to detect a shadow. The
        method uses two thresholds, a lower one that indicates a shadow and an
        upper threshold that when exceeded, indicates an increased background
        light level. Returns False unless the ratio of foreground to background
        is less than the threshold. A non-blocking method."""

        self._get_foreground()
        brightness_ratio = self._foreground / self._background
        if brightness_ratio < self._brightness_threshold:
            # Shadow detected; ratio is less than threshold
            return True
        elif brightness_ratio > 2 - self._brightness_threshold:
            # Background light level increased; refresh background measurement
            self.refresh_background()
        return False

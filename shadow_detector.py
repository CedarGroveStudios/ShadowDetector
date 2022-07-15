# Shadow Detector
# Copyright 2022 by JG for Cedar Grove Maker Studios
#
# gesture_detector.py 2022-07-15 v1.0715

import board
from analogio import AnalogIn

class ShadowDetector():
    """A CircuitPython class to detect a shadow cast over an analog
    light sensor such as the ALS-PT19 phototransistor used in the Adafruit
    PyPortal, PyGamer, PyBadge, CircuitPlayground Express, CircuitPlayground
    Bluefruit, and the ALS-PT19 breakout board. Useful as a simple gesture
    detector."""

    def __init__(self, pin, threshold=0.9, samples=2000, decay=0.01):
        """Class initializer. Instantiate the light sensor input and measure the
        initial background light level.

        :param board pin:   The light sensor's analog input pin.
        :param float threshold: The relative brightness threshold for shadow
                                detection. Defaults to 0.9, 90% of the foreground-
                                to-background brightness ratio. Range is 0.0
                                to 1.0.
        :param int samples: The number of samples needed for the _read method's
                            low-pass filter. Default is 2000 for a cut-off
                            frequency of approximately 25Hz when using a
                            SAMD-51 (M4) clocked at 120MHz. Range is any positive 
                            non-zero integer value.
        :param float decay: The magnitude of the forground-induced decay used to 
                            continuously adjust the background value each
                            time the foreground value is read. The decay compensates
                            for slowly changing background light levels. Default is
                            0.01, equivalent to a weight of 1 foreground sample per
                            99 background samples. Range is 0.0 to 1.0."""

        self._light_sensor = AnalogIn(pin)
        self._brightness_threshold = threshold
        self._samples = samples
        self._decay = max(min(decay, 1.0), 0.0)
        self.refresh_background()


    def _read(self):
        """Read and filter sensor level using a simple simple n-order finite 
        impulse response (FIR) moving-average (boxcar) low-pass filter."""
        measurement = 0
        for i in range(self._samples):
            measurement = measurement + (self._light_sensor.value / self._samples)
        return measurement


    def _get_foreground(self):
        """Read foreground sensor level and fractionally adjust the background
        level per the decay setting."""
        self._foreground = self._read()
        self._background = ((1.0 - self._decay) * self._background) + (self._decay * self._foreground)
        return


    def refresh_background(self):
        """Read background sensor level."""
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
            # Shadow detected; brightness ratio is less than threshold
            return True
        elif brightness_ratio > 2 - self._brightness_threshold:
            # Background light level increased; refresh background measurement
            self.refresh_background()
        return False

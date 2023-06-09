from math import *
import numpy as np
from .draw import Canvas


class ExtraCanvas(Canvas):
    """
    This is a subclass of the Canvas object with other functions for drawing other stuff that may never get into the main Canvas object.
    This way Canvas may not get very polluted bet there is still a place for certain ideas to exist.

    The description from Canvas:

    Essentially an audio output stream with basic drawing options.
    :param audio_device_index: The output device's index. See audio.get_all_device_info().
    :param rate: The sample rate of the stream. Default is 192000.
    :param record: Whether to temporarily store the frames, so they can be saved to a file later.
    :var audio: An instance of _audio._AudioBackend for simple audio outputting.
    :var frames: The frames to be written to the audio output.
    """
    def __init__(self, audio_device_index: int, rate: int = 192000, record: bool = False):
        super().__init__(audio_device_index, rate, record)

    def draw_butterfly(self, shift_x: int | float, shift_y: int | float,
                       scale_x: int | float = 2500, scale_y: int | float = 2500,
                       time: int | float = 20, step_t: int | float = 0.02, max_t: int | float = pi*20):
        """
        Draw a butterfly according to the parametric equations on https://mathworld.wolfram.com/ButterflyCurve.html.
        :param shift_x: The amount to shift by along the X-axis.
        :param shift_y: The amount to shift by along the Y-axis.
        :param scale_x: The amount to scale by along the X-axis. (May not represent the actual width.)
        :param scale_y: The amount to scale by along the Y-axis. (May not represent the actual height.)
        :param time: The total time to draw.
        :param step_t: In each frame, how many to increase the function's t variable by.
        :param max_t: The maximum amount t is allowed to get. Then the drawing of the butterfly will repeat as many times as needed.
        :return: The created frames.
        """
        t_array = np.arange(0, max_t, step_t)
        t_array_time = max_t / step_t / self.audio.get_rate()
        # region x = sin(t) * (e**cos(t)-2*cos(4*t)+sin(1/(12)t)**5)
        left = np.multiply(
            np.sin(t_array),
            np.add(
                np.subtract(
                    np.power(
                        e,
                        np.cos(t_array)
                    ),
                    np.multiply(
                        2,
                        np.cos(
                            np.multiply(
                                4,
                                t_array
                            )
                        )
                    )
                ),
                np.power(
                    np.sin(
                        np.divide(t_array, 12)
                    ),
                    5
                )
            )
        )
        # endregion
        # region y = cos(t) * (e**cos(t)-2*cos(4*t)+sin(1/(12)t)**5)
        right = np.multiply(
            np.cos(t_array),
            np.add(
                np.subtract(
                    np.power(
                        e,
                        np.cos(t_array)
                    ),
                    np.multiply(
                        2,
                        np.cos(
                            np.multiply(
                                4,
                                t_array
                            )
                        )
                    )
                ),
                np.power(
                    np.sin(
                        np.divide(t_array, 12)
                    ),
                    5
                )
            )
        )
        # endregion
        left, right = np.multiply(left, scale_x), np.multiply(right, scale_y)
        left, right = np.add(left, shift_x), np.add(right, shift_y)
        left, right = list(left), list(right)
        """frames = combed_frames * int(time / 1000 / t_array_time)
        frames += combed_frames[:int(time / 1000 % t_array_time / t_array_time * len(combed_frames))]
        OLD CODE KEPT FOR REFERENCE"""
        real_left = left * int(time / 1000 / t_array_time)
        real_left.extend(left[:int(time / 1000 % t_array_time / t_array_time * len(left))])
        real_right = right * int(time / 1000 / t_array_time)
        real_right.extend(right[:int(time / 1000 % t_array_time / t_array_time * len(right))])
        self._store_left_right(real_left, real_right)

    def effect_mosaic(self):
        pass


class _DevCanvas(Canvas):
    """
    This is a subclass of the Canvas object with functions that are unfinished.

    The description from Canvas:

    Essentially an audio output stream with basic drawing options.
    :param audio_device_index: The output device's index. See audio.get_all_device_info().
    :param rate: The sample rate of the stream. Default is 192000.
    :param record: Whether to temporarily store the frames, so they can be saved to a file later.
    :var audio: An instance of _audio._AudioBackend for simple audio outputting.
    :var frames: The frames to be written to the audio output.
    """

    def __init__(self, audio_device_index: int, rate: int = 192000, record: bool = False):
        super().__init__(audio_device_index, rate, record)

    def draw_spiral(self):
        """
        Draw an Archimedean spiral according to the parametric equations on https://mathworld.wolfram.com/ArchimedesSpiral.html.
        This is only an idea since I'm still in school and don't really understand how polar coordinates and trigonometry work.
        :return: The created frames
        """
        pass
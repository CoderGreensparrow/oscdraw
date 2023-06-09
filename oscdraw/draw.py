from collections.abc import Collection
import math
from typing import Literal
from unicodedata import normalize
from ._audio import _AudioBackend
from .objects import Point, Line, Polygon, Ellipse, ObjectCollection, degrees_to_radians
from .font import Font, default_font
import numpy as np


class Canvas:
    """
    Essentially an audio output stream with basic drawing options.
    Every time "frames" are referenced, the frames are not actually stored in a single list, but there are two lists,
    one for the left channel and one for the right channel. In the end, the two are combed together to create actual frames.
    The documentation is from an older version that actually had a self.frames variable.
    :param audio_device_index: The output device's index. See audio.get_all_device_info().
    :param rate: The sample rate of the stream. Default is 192000.
    :param record: Whether to temporarily store the frames, so they can be saved to a file later.
    :var audio: An instance of _audio._AudioBackend for simple audio outputting.
    :var left: The frames to be written to the audio output, only the left channel.
    :var right: The frames to be written to the audio output, only the right channel.
    """
    def __init__(self, audio_device_index: int = None, rate: int = 192000, record: bool = False):
        self.audio = _AudioBackend(audio_device_index, rate=rate, record=record)
        self.left, self.right = [], []
        self._last_left, self._last_right = [], []

    @staticmethod
    def _comb_left_right(left, right):
        """
        Comb the left and right channels into an array with 1 dimension for internal use.
        :param left: The left channel.
        :param right: The right channel.
        :return: The combed array.
        """
        frames = []
        for i in range(len(left)):
            frames.append(left[i])
            frames.append(right[i])
        return frames

    def _store_left_right(self, left, right):
        """
        Store the created left and right channel values for internal use.
        :param left: The left channel's new values.
        :param right: The right channel's new values.
        :return: None
        """
        if not (isinstance(left, tuple) or isinstance(left, list)): left = tuple(left)
        if not (isinstance(right, tuple) or isinstance(right, list)): right = tuple(right)
        self.left.extend(left)
        self.right.extend(right)
        self._last_left = left
        self._last_right = right

    def _handle_supports_last(self, last: bool):
        """
        Handle the setup of functions that support the last argument. (change_shift etc.)
        :param last: Value of last
        :return: left, right
        """
        if not last:
            left, right = self.left.copy(), self.right.copy()
            self.left.clear()
            self.right.clear()
        else:
            self.left = self.left[:len(self.left) - len(self._last_left)]  # Remove _last_left with slices
            self.right = self.right[:len(self.right) - len(self._last_right)]  # Remove _last_right with slices
            left, right = self._last_left, self._last_right
        return left, right

    def get_left_right(self):
        """
        Return the frames by the two channels.
        :return: Left, right.
        """
        return self.left, self.right

    def get_last(self):
        """
        Return the last frames by the two channels.
        :return: Left, right.
        """
        return self._last_left, self._last_right

    def repeat(self, amount: int = 1):
        """
        How many times to add the previous frames to all the frames.
        :param amount: The amount of times to add, default is 1.
        :return: None
        """
        self.left.extend(self._last_left * amount)
        self._last_left.extend(self._last_left * amount)
        self.right.extend(self._last_right * amount)
        self._last_right.extend(self._last_right * amount)

    def draw_point(self, point: Point | Collection[int, int]):
        """
        Draws a point on the oscilloscope.
        :param point: The point. See the Point class for more details.
        :return: None
        """
        if not isinstance(point, Point): point = Point(point)
        left, right = [], []
        left.append(point.x)
        right.append(point.y)
        self._store_left_right(left, right)

    def draw_line(self, line: Line | Collection[Point, Point] | Collection[[int, int], [int, int]] | Collection[int, int, int, int],
                  frequency: int | float, time: int | float, mode: Literal["square", "sawtooth", "triangle"] = "sawtooth"):
        """
        Draw a line on the oscilloscope.
        :param line: The line. See the Line class for more details.
        :param frequency: The frequency of the wave.
        :param time: The length of drawing the line, in milliseconds.
        :param mode: The type of waves to draw the line with (may not be perfect waves).
        :return: None
        """
        if not isinstance(line, Line): line = Line(line)
        left, right = [], []
        num_frames = int(self.audio.get_rate() * time / 1000)
        if num_frames == 0:
            raise ValueError(
                f"With the given values, the line cannot be drawn\n"
                f"Consider increasing the time to draw or the sample rate"
            )
        frames_per_cycle = self.audio.get_rate() / frequency
        if mode == "square":
            for i in range(num_frames):
                if i % frames_per_cycle / frames_per_cycle < 0.5:
                    left.append(line.p1.x)
                    right.append(line.p1.y)
                else:
                    left.append(line.p2.x)
                    right.append(line.p2.y)
        elif mode == "sawtooth":
            for i in range(num_frames):
                percent = i % (frames_per_cycle + 1/frames_per_cycle) / (frames_per_cycle + 1/frames_per_cycle)
                current_point = Point(
                    (line.p2.x - line.p1.x) * percent + line.p1.x,
                    (line.p2.y - line.p1.y) * percent + line.p1.y
                )
                left.append(current_point.x)
                right.append(current_point.y)
        elif mode == "triangle":
            for i in range(num_frames):
                percent = i*2 % (frames_per_cycle + 1/frames_per_cycle) / (frames_per_cycle + 1/frames_per_cycle)
                if i % frames_per_cycle / frames_per_cycle < 0.5:
                    current_point = Point(
                        (line.p2.x - line.p1.x) * percent + line.p1.x,
                        (line.p2.y - line.p1.y) * percent + line.p1.y
                    )
                else:
                    current_point = Point(
                        (line.p2.x - line.p1.x) * (1-percent) + line.p1.x,
                        (line.p2.y - line.p1.y) * (1-percent) + line.p1.y
                    )
                left.append(current_point.x)
                right.append(current_point.y)
        else:
            raise ValueError(
                f"Unknown line drawing mode: {mode}"
            )
        self._store_left_right(left, right)

    def draw_lines(self, lines: Collection[Line, ...] | Collection[...],
                   frequency: int | float, time: int | float, mode: Literal["square", "sawtooth", "triangle"] = "sawtooth"):
        """
        Draw multiple lines.
        :param lines: The lines in a collection. See the Line class for line representations.
        :param frequency: The frequency of each line.
        :param time: The total time to draw every line one after the other.
        :param mode: The type of waves to draw the lines with (may not be perfect waves).
        :return: None
        """
        lines = list(lines)
        for i, line in enumerate(lines):
            if not isinstance(line, Line):
                lines[i] = Line(line)
        left, right = [], []
        time_per_line = time / len(lines)
        for line in lines:
            self.draw_line(line, frequency, time_per_line, mode)
            left.extend(self._last_left)
            right.extend(self._last_right)
        self._last_left = left
        self._last_right = right

    def draw_polygon(self, polygon: Polygon | Collection[Point, ...] | Collection[...],
                     frequency: int | float, time: int | float, mode: Literal["square", "sawtooth", "triangle"] = "sawtooth"):
        """
        Draw a polygon.
        :param polygon: The polygon. A Polygon object, a list of Point objects, or a list with point representations. See the Point class for more details.
        :param frequency: The frequency of each line (side) of the polygon.
        :param time: The total time to draw the polygon (each side one after the other).
        :param mode: The type of waves to draw the lines (sides) with (may not be perfect waves).
        :return: None
        """
        if not isinstance(polygon, Polygon):
            polygon = list(polygon)
            for i, point in enumerate(polygon):
                if not isinstance(point, Point):
                    polygon[i] = Point(point)
            polygon = Polygon(*polygon)
        lines = polygon.get_lines()
        self.draw_lines(lines, frequency, time, mode)
        # No need to set _last_left and _last_right, since we only call self.draw_lines() once and that already sets it

    def draw_ellipse(self, ellipse: Ellipse | Collection[Point, int | float, int | float] | Collection[[int | float, int | float], int | float, int | float] | Collection[int | float, int | float, int | float, int | float],
                     frequency: int | float, time: int | float, distort_rotate: int | float = None):
        """
        Draw an ellipse.
        :param ellipse: The ellipse. An Ellipse object, or other representations of an ellipse. See the Ellipse class for more details.
        :param frequency: The frequency of the sine and cosine waves.
        :param time: The total time to draw the ellipse for.
        :param distort_rotate: Rotate the sine wave of the left channel by some degrees. Default is 0, no rotation.
        :return: None
        """
        if not isinstance(ellipse, Ellipse): ellipse = Ellipse(ellipse)
        tau = np.pi*2
        frames_per_cycle = self.audio.get_rate() / frequency
        frequency_list = np.arange(0, self.audio.get_rate() * (time / 1000) / frames_per_cycle * tau, tau/frames_per_cycle)  # TODO: Rethink how this works (it does maybe)
        sine_list = np.sin(frequency_list)
        if distort_rotate:
            angle = degrees_to_radians(distort_rotate)
            frequency_list = np.add(frequency_list, angle)
        cosine_list = np.cos(frequency_list)
        left = np.multiply(cosine_list, ellipse.width/2)
        right = np.multiply(sine_list, ellipse.height/2)
        left = np.add(left, ellipse.centre.x)
        right = np.add(right, ellipse.centre.y)
        self._store_left_right(left, right)

    def draw_object_collection(self, obj: ObjectCollection, frequency: int | float, time: int | float,
                               line_mode: Literal["square", "sawtooth", "triangle"] = "sawtooth"):
        """
        Draw an ObjectCollection object.
        :param obj: The ObjectCollection object.
        :param frequency: The frequency passed to every object.
        :param time: The total time to draw everything in milliseconds.
        :param line_mode: The line drawing mode. See self.draw_line() for more.
        :return: None
        """
        time_per_object = time / len(obj.modified_objects)
        left, right = [], []
        for object in obj.modified_objects:
            if isinstance(object, Point):
                self.draw_point(object)
                self.repeat(self.audio.get_rate()*(time_per_object/1000))
            elif isinstance(object, Line):
                self.draw_line(object, frequency, time_per_object, line_mode)
            elif isinstance(object, Polygon):
                self.draw_polygon(object, frequency, time, line_mode)
            elif isinstance(object, Ellipse):
                self.draw_ellipse(object, frequency, time_per_object)
            elif isinstance(object, ObjectCollection):
                self.draw_object_collection(object, frequency, time_per_object, line_mode)
            left.extend(self._last_left)
            right.extend(self._last_right)
        self._last_left, self._last_right = left, right

    def draw_font(self, text: str, x: int | float, y: int | float, frequency: int | float, time: int | float, line_mode: Literal["square", "sawtooth", "triangle"] = "sawtooth",
                  character_width=5000, character_height=5000, character_spacing=0, line_spacing=2500, font: Font = None):
        """
        Draws a text with a font (specialized for this purpose).
        :param text: The string to draw.
        :param x: The X-position of the top left position of the text.
        :param y: The Y-position of the top left position of the text.
        :param frequency: The frequency of every drawn object (those who take frequency that is).
        :param time: The time to draw each character (not the whole text) in milliseconds.
        :param line_mode: The line drawing mode. See self.draw_line() for more.
        :param character_width: The width of a character. For full-width characters, the character_height is used, default is 5000.
        :param character_height: The height of a character, default is 5000.
        :param character_spacing: The spacing of the characters, default is 0.
        :param line_spacing: The spacing of the lines, default is 2500.
        :param font: Defines a custom, specialized-to-be-used-in-this-function font. Default is None, a built-in font is used.
        :return: None
        """
        if font is None: font = default_font
        text = normalize("NFD", text)
        start_x = x
        x, y = x, y
        left, right = [], []
        for char in text:
            if char == "\n":
                y -= character_height + line_spacing
                x = start_x
            elif char == "\t":
                x += 2 * (character_width + character_spacing)
            else:
                obj = font._get_character(char, x, y, character_width, character_height)
                if obj:
                    self.draw_object_collection(obj, frequency, time, line_mode)
                    left.extend(self._last_left)
                    right.extend(self._last_right)
                x += character_width + character_spacing
        self._last_left = left
        self._last_right = right

    def change_shift(self, x, y, last: bool = True):
        """
        Shift all the frames or only the last action's frames.
        :param x: Amount on the X-axis.
        :param y: Amount on the Y-axis.
        :param last: Whether to change only the last action's frames or to change all the frames stored so far. Default is True (so first option).
        :return: None
        """
        left, right = self._handle_supports_last(last)
        left = np.add(left, x)
        right = np.add(right, y)
        self._store_left_right(left, right)

    def change_rotate(self, angle: int | float, centre: Point | Collection[int | float, int | float] = None,
                      last: bool = True):
        """
        Rotate all the frames or only the last action's frames.
        :param angle: The angle to rotate by in degrees.
        :param centre: The centre of rotation as a Point object or other point representations, see the Point class for more details.
        :param last: Whether to change only the last action's frames or to change all the frames stored so far. Default is True (so first option).
        :return: None
        """
        if centre is None: centre = Point(0, 0)
        elif not isinstance(centre, Point): centre = Point(centre)
        angle = degrees_to_radians(angle)

        left, right = self._handle_supports_last(last)
        left = list(np.subtract(left, centre.x))
        right = list(np.subtract(right, centre.y))
        for i in range(len(left)):
            left[i], right[i] = np.dot([left[i], right[i]],
                          [[math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]])
        left = np.add(left, centre.x)
        right = np.add(right, centre.y)
        self._store_left_right(left, right)

    def change_scale(self, x: int | float, y: int | float,
                     centre: Point | Collection[int | float, int | float] = None, last: bool = True):
        """
        Rotate all the frames or only the last action's frames.
        :param x: The amount to scale by on the X-axis.
        :param y: The amount to scale by on the Y-axis.
        :param centre: The centre of scaling as a Point object or other point representations, see the Point class for more details.
        :param last: Whether to change only the last action's frames or to change all the frames stored so far. Default is True (so first option).
        :return: None
        """
        if centre is None: centre = Point(0, 0)
        elif not isinstance(centre, Point): centre = Point(centre)

        left, right = self._handle_supports_last(last)
        left = np.subtract(left, centre.x)
        right = np.subtract(right, centre.y)
        left = np.multiply(left, x)
        right = np.multiply(right, y)
        left = np.add(left, centre.x)
        right = np.add(right, centre.y)
        self._store_left_right(left, right)

    def change_clip(self, clip_left: int | float = math.inf, clip_right: int | float = math.inf,
                    clip_top: int | float = math.inf, clip_bottom: int | float = math.inf, last: bool = True):
        """
        Clip (clamp) the values of the frames.
        :param clip_left: The minimum value along the X-axis.
        :param clip_right: The maximum value along the X-axis.
        :param clip_top: The maximum value along the Y-axis.
        :param clip_bottom: The minimum value along the Y-axis.
        :param last: Whether to change only the last action's frames or to change all the frames stored so far. Default is True (so first option).
        :return: None
        """
        left, right = self._handle_supports_last(last)
        left = np.clip(left, clip_left, clip_right)
        right = np.clip(right, clip_bottom, clip_top)
        self._store_left_right(left, right)

    def change_cut_out_of_limits(self, limit_left: int | float = math.inf, limit_right: int | float = math.inf,
                                 limit_top: int | float = math.inf, limit_bottom: int | float = math.inf, last: bool = True):
        """
        Cut off values that are lower than the limits.
        :param limit_left: The minimum value along the X-axis.
        :param limit_right: The maximum value along the X-axis.
        :param limit_top: The maximum value along the Y-axis.
        :param limit_bottom: The minimum value along the Y-axis.
        :param last: Whether to change only the last action's frames or to change all the frames stored so far. Default is True (so first option).
        :return: None
        """
        left, right = self._handle_supports_last(last)
        i = 0
        while i < len(left):
            if (left[i] < limit_left or limit_right < left[i]) or (right[i] < limit_bottom or limit_top < right[i]):
                left.pop(i)
                right.pop(i)
            else:
                i += 1
        self._store_left_right(left, right)

    def change_cut_to_length(self, max_draw_time, beginning: bool = True):
        """
        Cut off from the total frames that will be drawn, so it could be drawn under some set time.
        :param max_draw_time: The maximum allowed time to draw in milliseconds.
        :param beginning: Whether to cut from the beginning or the end. Default is True (so beginning).
        :return: None
        """
        left, right = self.left.copy(), self.right.copy()
        self.left.clear()
        self.right.clear()
        max_frame_num = int(max_draw_time / 1000 * self.audio.get_rate())
        if len(left) > max_frame_num:
            if beginning:
                left_cut = left[:max_frame_num - 1]
                right_cut = right[:max_frame_num - 1]
                left = left[-max_frame_num:]
                right = right[-max_frame_num:]
            else:
                left_cut = left[-max_frame_num + 1:]
                right_cut = right[-max_frame_num + 1:]
                left = left[:max_frame_num]
                right = right[:max_frame_num]
            self._store_left_right(left, right)
            self._last_left, self._last_right = left_cut, right_cut

    def write(self, clear=True):
        """
        Write the frames stored to the stream.
        :param clear: Whether to remove the stored frames. Default is True.
        :return: The written frames.
        """
        frames = self._comb_left_right(self.left, self.right)
        self.audio.write(frames)
        if clear:
            self.left.clear()
            self.right.clear()
        return frames

    def clear(self):
        """
        Clear the frames stored without writing.
        :return: None
        """
        self.left.clear()
        self.right.clear()

"""
Visualize frames of audio data to-be-written or read from an input.
"""
import numpy as np
from typing import Literal
from .draw import Canvas
from ._audio import _AudioBackend
try:
    import pygame
    pygame.init()
    pygame.font.init()
    pygame_enabled = True
except ImportError:
    pygame_enabled = False
try:
    import matplotlib.pyplot as plt
    plt_enabled = True
except ImportError:
    plt_enabled = False


class _ViewBase:
    """
    Base class for other views.
    :param source: The source of the frames of audio, a draw.Canvas or an _audio._AudioBackend.
    :param num_of_read_frames: If the source is an _audio._AudioBackend, then this value will be given to _AudioBackend.read().
    """
    def __init__(self, source: Canvas | _AudioBackend, num_of_read_frames: int = 192000 // 60):
        if not (isinstance(source, Canvas) or isinstance(source, _AudioBackend)):
            raise TypeError(
                f"Cannot read source from an object of type: {type(source)}"
            )
        self.source = source
        self.left, self.right = [], []
        self.read_frames = num_of_read_frames

    def _get_left_right(self, frames):
        left = [i for i in range(0, len(frames)-1, 2)]
        right = [i for i in range(1, len(frames), 2)]
        return left, right

    def _get_frames(self):
        """
        Get the frames from the source and set it to be in self.frames.
        :return: None
        """
        if isinstance(self.source, Canvas):
            self.left, self.right = self.source.left, self.source.right
        elif isinstance(self.source, _AudioBackend):
            frames = self.source.read(self.read_frames)
            self.left, self.right = self._get_left_right(frames)


OSCILLOSCOPE_VIEW_DEFAULT_PARAMS = {
    "background_color": "#000000",
    "line_color": "#2BFF66",
    "line_width": 1,
    "debug_font": "sans-serif",
    "debug_font_size": 18,
    "debug_color": "#EEEEEE",
    "draw_debug_background": False,
    "debug_background": "#000000"
}
"""The default other params for OscilloscopeView."""


class OscilloscopeView(_ViewBase):
    """
    An oscilloscope-like visualization of frames of audio with pygame.
    :param source: The source of the frames of audio, a draw.Canvas or an _audio._AudioBackend.
    :param num_of_read_frames: If the source is an _audio._AudioBackend, then this value will be given to _AudioBackend.read().
    :param window_size: The size of the pygame window (by the way, the window is resizable and sized).
    :param debug_data_in_window: Show FPS, number of frames and possibly other info in the window.
    :param params: Any modifications to other parameters in a dictionary. To see the defaults, look in audioview.py for OSCILLOSCOPE_VIEW_DEFAULT_PARAMS.
    """
    def __init__(self, source: Canvas | _AudioBackend, num_of_read_frames: int = 192000 // 60,
                 window_size: tuple[float, float] = (800, 800), debug_data_in_window: bool = False,
                 params: dict = None):
        if not pygame_enabled:
            raise ModuleNotFoundError(
                f"pygame could not be imported"
            )
        super().__init__(source, num_of_read_frames)
        self.size = window_size
        self.debug = debug_data_in_window
        self.params = OSCILLOSCOPE_VIEW_DEFAULT_PARAMS
        if params: self.params.update(params)
        self.window = pygame.display.set_mode(window_size, pygame.RESIZABLE | pygame.SCALED)
        self.debug_font = pygame.font.SysFont(self.params["debug_font"], self.params["debug_font_size"])
        self.clock = pygame.time.Clock()

    def update(self):
        self.clock.tick()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        self._get_frames()
        left, right = self.left, self.right
        # region SET UP VARIABLES FOR EASIER ACCESS
        bg = self.params["background_color"]
        line_c = self.params["line_color"]
        line_w = self.params["line_width"]
        # self.debug_font
        debug_c = self.params["debug_color"]
        draw_debug_bg = self.params["draw_debug_background"]
        debug_bg = self.params["debug_background"]
        #  extra_debug = self.params["show_extra_debug_info"]
        # endregion
        min_window_size = min(*self.size)
        left = np.multiply(left, min_window_size/2**15*0.5)
        right = np.multiply(right, min_window_size/2**15*-0.5)
        left = np.add(left, min_window_size/2)
        right = np.add(right, min_window_size/2)
        self.window.fill(bg)
        pygame.draw.aalines(self.window, line_c, False, tuple(zip(left, right)))
        if self.debug:
            info = {
                "FPS": round(self.clock.get_fps()*100)/100,
                "len of left": len(self.left),
                "len of right": len(self.right)
            }
            for i, keyval in enumerate(info.items()):
                key, val = keyval
                render = self.debug_font.render(f"{key}: {val}", True, debug_c, debug_bg if draw_debug_bg else None)
                #  render.blit(self.window, )
                self.window.blit(render, (10, 10 + i * self.debug_font.get_linesize()))
        pygame.display.flip()


class AudioPlotView(_ViewBase):
    def __init__(self, source: Canvas | _AudioBackend, num_of_read_frames: int = 192000 // 60,
                 include: Literal["lr", "l", "r"] = "lr", left_plot_kwargs: dict = None, right_plot_kwargs: dict = None):
        """
        Simple plot visualization of frames of audio. Doesn't update in real time.
        :param source: The source of the frames of audio, a draw.Canvas or an _audio._AudioBackend.
        :param num_of_read_frames: If the source is an _audio._AudioBackend, then this value will be given to _AudioBackend.read().
        :param include: What channels to include in the visualization. "lr" for both, "l" for left, "r" for right. This option can be overridden in the self.plot() function.
        :param left_plot_kwargs: Any keyword arguments to be passed to plt.plot() for the left channel's plot.
        :param right_plot_kwargs: Any keyword arguments to be passed to plt.plot() for the right channel's plot.
        """
        super().__init__(source, num_of_read_frames)
        self.include = include
        self.left_kwargs = {
            "color": "blue",
            "linestyle": "dashed" if include == "lr" else "solid",
            "zorder": 1
        }
        self.right_kwargs = {
            "color": "red",
            "linestyle": "dashed" if include == "lr" else "solid",
            "zorder": 0
        }
        if left_plot_kwargs: self.left_kwargs.update(left_plot_kwargs)
        if right_plot_kwargs: self.right_kwargs.update(right_plot_kwargs)

    def plot(self, include: Literal["lr", "l", "r"] = None):
        if include is None: include = self.include
        self._get_frames()
        left, right = self.left, self.right
        if include in ("l", "lr"):
            plt.plot(left, **self.left_kwargs)
        if include in ("r", "lr"):
            plt.plot(right, **self.right_kwargs)
        plt.title("Plot of " + ("left" if include == "l" else "left and right" if include == "lr" else "right") + " channels" if include == "lr" else " channel")
        plt.ylabel("Value")
        plt.xlabel("Position")
        plt.show()
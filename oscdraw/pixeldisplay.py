from .draw import Canvas

class BWDisplay:
    """
    A black and white "pixel display". Only black and white.
    """
    def __init__(self, canvas: Canvas, size: tuple[int, int]):
        self.c = canvas
        self.width, self.height = size
        self.pixels = []

    def update(self, pixels: list[bool], downscale: int = None):
        """
        Update the display with new pixel data.
        :param pixels:
        :param downscale: Downscale amount (how long is the side of the square that contains the pixels to be merged).
        :return: None
        """
        self.pixels = pixels.copy()

    def draw(self, shift_x=0, shift_y=0, scale_x=1, scale_y=1, skip_pixels: int = 0, skip_lines: int = 0, canvas: Canvas = None):
        """
        Draw the pixels to the canvas.
        :param shift_x: How much to shift the center on the X axis.
        :param shift_y: How much to shift the center on the Y axis.
        :param scale_x: How much to scale on the X axis.
        :param scale_y: How much to scale on the Y axis.
        :param skip_pixels: How many pixels to skip in each line. Default is 0.
        :param skip_lines: How many lines to skip every line. Default is 0.
        :param canvas: The canvas to draw onto. If None, the default is used.
        :return: None
        """
        c = canvas if canvas else self.c
        width, height = self.width, self.height
        for i, pixel in enumerate(self.pixels):
            if (i // self.width) % (skip_lines + 1) != 0:
                continue
            elif (i % self.width) % (skip_pixels + 1) != 0:
                continue
            if pixel:
                x, y = i % width - width // 2, height // 2 - i // width
                x, y = (x + shift_x) * scale_x, (y + shift_y) * scale_y
                c.draw_point((x, y))

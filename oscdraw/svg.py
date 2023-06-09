"""
Construct objects.ObjectCollection objects from svg files.
As of now, drawing Bézier curves is not possible.
Instead, points are drawn one by one to approximate a Bézier curve.
(Thanks to svg.path having the point() function on CubicBezier and QuadraticBezier objects too.)
"""

from svgpathtools import svg2paths2

from ._disabled_module import disable_module
disable_module(True)

class Svg:
    def __init__(self, filepath: str):
        """
        Construct objects.ObjectCollection objects from svg files.
        As of now, drawing Bézier curves is not possible.
        Instead, points are drawn one by one to approximate a Bézier curve. (Wait a minute... isn't that the same thing?)
        (Thanks to svg.path having the point() function on CubicBezier and QuadraticBezier objects too.)
        :param filepath: The path to a file
        """
        self.file = filepath
        self.paths = svg2paths2(self.file)
        self.obj_cache = None

    def get_object_collection(self):
        if self.obj_cache is None:
            #  for
            pass
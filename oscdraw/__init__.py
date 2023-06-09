"""
A package for drawing stuff on an oscilloscope in real time!
Using this package and others you could make a game for the oscilloscope!

-------------------------------------------------------------------------

**Required dependencies:**

- *numpy*
- *pyaudio*
- *wave* (built-in)
- *math* (built-in)
- *os* (built-in)
- *copy* (built-in)
- *importlib* (built-in)
- *logging* (built-in)
- *typing* (built-in)
- *collections* (built-in)
- *unicodedata* (built-in)

**Optional dependencies:**

- *pygame*
- *matplotlib*
- *svgpathtools*

**Optional dependencies for demos:*

- *keyboard*

And any other dependencies are also required/optional that these need.
"""

from .draw import Canvas
from .objects import Point, Line, Polygon, Ellipse, ObjectCollection, PointTools
import logging
from importlib.machinery import PathFinder

p = PathFinder()

for name in ("numpy", "pyaudio", "wave", "os", "copy", "typing", "collections", "unicodedata"):
    if p.find_spec(name) is None:
        raise ModuleNotFoundError(
            f"dependency not found: '{name}'"
        )

optionals = {
    "pygame": "audioview.OscilloscopeView will not work.",
    "matplotlib": "audioview.AudioPlotView will not work.",
    "svgpathtools": "the svg module will not work."
}
for name, warn in optionals.items():
    if p.find_spec(name) is None:
        logging.warning(
            f"Optional dependency {name} not found: {warn}"
        )
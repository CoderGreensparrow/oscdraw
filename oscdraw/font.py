"""
A Font class and a built-in default font for usage in Canvas.draw_font().
"""
from collections.abc import Mapping
import copy
from .objects import Point, Line, Polygon, Ellipse, ObjectCollection


class Font:
    """
    Represents a font specifically used in Canvas.draw_font().

    A font is essentially a dict object with the keys being the letters or characters and the values being ObjectCollection objects that tell what things to use to draw the character.
    The coordinates given in the letters are: X-axis 0 - 1000, Y-axis 0 - -1000. The origin point is in the top left corner.
    All letters have a box space, but each letter can be scaled in code. The spacing between letters could also be controlled, but the default is 0.*
    If an unknown character is encountered, it is skipped.

    *The line spacing is only controlled in code.
    :param font: The font in a dict. Read the above description for more info.
    """
    def __init__(self, font: Mapping[str, ObjectCollection]):
        self.font = font

    def _get_character(self, char: str, x: int | float, y: int | float, width: int | float = 1000, height: int | float = 1000):
        """
        Get a character (ObjectCollection) for a specific position and scaling.
        :param char: The character. Not parsed in this function.
        :param x: The top left X-position.
        :param y: The top left Y-position.
        :param width: Default 1000.
        :param height: Default 1000.
        :return: The positioned and scaled ObjectCollection. None if character is not found.
        """
        if char in self.font:
            obj = copy.deepcopy(self.font[char])
            obj.scale(width/1000, height/1000)
            obj.shift(x, y)
            return obj
        else:
            return None

    def __repr__(self):
        text = "Font {\n"
        for char, objects in self.font.items():
            text += f"    '{char}': {objects}\n"
        text += "}"
        return text

default_font = Font({
    "A": ObjectCollection(Line((0, -1000, 400, 0)), Line((400, 0, 800, -1000)), Line((200, -500, 600, -500))),
    "B": ObjectCollection(Polygon((0, -500), (0, 0), (700, 0), (800, -250), (700, -500), (0, -500), (0, -1000), (700, -1000), (800, -750), (700, -500))),
    "C": ObjectCollection(Line((800, -250, 400, 0)), Line((400, 0, 0, -250)), Line((0, -250, 0, -750)), Line((0, -750, 400, -1000)), Line((400, -1000, 800, -750))),
    "D": ObjectCollection(Polygon((0, 0), (0, -1000), (700, -1000), (800, -750), (800, -250), (700, 0))),
    "E": ObjectCollection(Line((0, 0, 0, -1000)), Line((0, 0, 800, 0)), Line((0, -500, 600, -500)), Line((0, -1000, 800, -1000))),
    "F": ObjectCollection(Line((0, 0, 0, -1000)), Line((0, 0, 800, 0)), Line((0, -500, 600, -500))),
    "G": ObjectCollection(Line((800, -250, 400, 0)), Line((400, 0, 0, -250)), Line((0, -250, 0, -750)), Line((0, -750, 400, -1000)), Line((400, -1000, 800, -750)), Line((800, -750, 400, -750))),
    "H": ObjectCollection(Line((0, 0, 0, -1000)), Line((0, -500, 800, -500)), Line((800, 0, 800, -1000))),
    "I": ObjectCollection(Line((400, 0, 400, -1000))),
    "J": ObjectCollection(Line((400, 0, 400, -800)), Line((400, -800, 200, -1000)), Line((200, -1000, 0, -800))),
    "K": ObjectCollection(Line((0, 0, 0, -1000)), Line((0, -500, 800, 0)), Line((0, -500, 800, -1000))),
    "L": ObjectCollection(Line((0, 0, 0, -1000)), Line((0, -1000, 800, -1000))),
    "M": ObjectCollection(Line((0, -1000, 0, 0)), Line((0, 0, 400, -400)), Line((400, -400, 800, 0)), Line((800, 0, 800, -1000))),
    "N": ObjectCollection(Line((0, -1000, 0, 0)), Line((0, 0, 800, -1000)), Line((800, -1000, 800, 0))),
    "O": ObjectCollection(Ellipse((400, -500, 800, 1000))),
    "P": ObjectCollection(Line((0, 0, 0, -1000)), Ellipse((400, -250, 800, 500))),
    "Q": ObjectCollection(Ellipse((400, -500, 800, 1000)), Line((600, -600, 800, -1000))),
    "R": ObjectCollection(Line((0, 0, 0, -1000)), Ellipse((400, -250, 800, 500)), Line((400, -500, 800, -1000))),
    "S": ObjectCollection(Line((800, -250, 400, 0)), Line((400, 0, 0, -250)), Line((0, -250, 800, -750)), Line((800, -750, 400, -1000)), Line((400, -1000, 0, -750))),
    "T": ObjectCollection(Line((0, 0, 800, 0)), Line((400, 0, 400, -1000))),
    "U": ObjectCollection(Line((0, 0, 0, -800)), Line((0, -800, 400, -1000)), Line((400, -1000, 800, -800)), Line((800, -800, 800, 0))),
    "V": ObjectCollection(Line((0, 0, 400, -1000)), Line((400, -1000, 800, 0))),
    "W": ObjectCollection(Line((0, 0, 200, -1000)), Line((200, -1000, 400, -200)), Line((400, -200, 600, -1000)), Line((600, -1000, 800, 0))),
    "X": ObjectCollection(Line((0, 0, 800, -1000)), Line((0, -1000, 800, 0))),
    "Y": ObjectCollection(Line((0, 0, 400, -500)), Line((400, -500, 800, 0)), Line((400, -500, 400, -1000))),
    "Z": ObjectCollection(Line((0, 0, 800, 0)), Line((800, 0, 0, -1000)), Line((0, -1000, 800, -1000))),
    "1": ObjectCollection(Line((0, -500, 400, 0)), Line((400, 0, 400, -1000))),
    "2": ObjectCollection(Line((0, -400, 400, 0)), Line((400, 0, 800, -400)), Line((800, -400, 0, -1000)), Line((0, -1000, 800, -1000))),
    "3": ObjectCollection(Line((0, 0, 800, 0)), Line((800, 0, 400, -500)), Line((400, -500, 800, -400)), Line((800, -400, 800, -800)), Line((800, -800, 400, -1000)), Line((400, -1000, 0, -800))),
    "4": ObjectCollection(Line((400, 0, 0, -750)), Line((0, -750, 800, -750)), Line((400, -500, 400, -1000))),
    "5": ObjectCollection(Line((800, 0, 0, 0)), Line((0, 0, 0, -500)), Line((0, -500, 700, -500)), Line((700, -500, 800, -750)), Line((800, -750, 700, -1000)), Line((700, -1000, 0, -1000))),
    "6": ObjectCollection(Line((400, 0, 0, -750)), Ellipse((400, -750, 800, 500))),
    "7": ObjectCollection(Line((0, 0, 800, 0)), Line((800, 0, 0, -1000))),
    "8": ObjectCollection(Ellipse((400, -250, 700, 500)), Ellipse((400, -750, 800, 500))),
    "9": ObjectCollection(Ellipse((400, -250, 800, 500)), Line((800, -250, 400, -1000))),
    "0": ObjectCollection(Ellipse((400, -500, 700, 1000)), Line((100, -850, 700, -150))),
    ".": ObjectCollection(Ellipse((50, -950, 100, 100))),
    ":": ObjectCollection(Ellipse((50, -950, 100, 100)), Ellipse((50, -450, 100, 100))),
    ",": ObjectCollection(Line((100, -800, -100, -1100))),
    "!": ObjectCollection(Line((50, 0, 50, -800)), Ellipse((50, -950, 100, 100))),
    "?": ObjectCollection(Line((0, -250, 300, 0)), Line((300, 0, 600, -250)), Line((600, -250, 300, -500)), Line((300, -500, 300, -800)), Ellipse((300, -950, 100, 100)))
})
"""The default font in this package."""

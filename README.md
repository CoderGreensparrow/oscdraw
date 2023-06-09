# oscdraw
Draw things on an oscilloscope live with code.

A package for drawing stuff on an oscilloscope in real time!
By using this package and others, you could make a game for the oscilloscope!

-----------------------------------------------------------------------------

# Installation

Just download the folder `oscdraw` and move it to your project folder. Python should recognize it as a package.

## Dependencies

**Required dependencies:**

- `numpy`
- `pyaudio*
- `wave` (built-in)
- `math` (built-in)
- `os` (built-in)
- `copy` (built-in)
- `importlib` (built-in)
- `logging` (built-in)
- `typing` (built-in)
- `collections` (built-in)
- `unicodedata` (built-in)

**Optional dependencies:**

- `pygame`
- `matplotlib`
- `svgpathtools`

**Optional dependencies for demos:*

- `keyboard`

And any other dependencies are also required/optional that these need.

# Usage

The package contains multiple modules. The main modules you should focus on are: `draw`, `objects`, `font`.

## `draw`

The draw module contains the `Canvas` object, which represents a "canvas" you can draw lines, ellipses and other objects on.
The canvas could be outputted through an audio channel. **The audio channel must have 2 channels.**

The functions in `Canvas` starting with `draw_` are the functions for drawing. Use the appropriate function from your linter.

You can observe, that some functions ask for objects of type `Point`, `Line` etc. See the `objects` module below.

## `objects`

These classes are abstract representations of objects. Using these are recommended if you don't use any shortenings (see the shortenings section for more).
Make sure you pass the appropriate objects to the appropriate `draw_` functions.

## `font`

If you want to create your custom font for the `draw_font` function (e.g. one that supports cyrillic or japanese characters), use the `Font` class. Make sure you understand how to use `ObjectCollection`s from `objects`.

## shortenings

A shortening is just a shorter way to pass the values to functions.
E.g. for the `draw_line` function:

- `draw_line(Line(Point(0, 0), Point(1000, 1000)))`
- `draw_line(Line((0, 0), (1000, 1000))`
- `draw_line((0, 0, 1000, 1000))`

All of these are valid code. As you can see, the last one is the shortest. Use your linter to get to know what your options are.

# Emulating an oscilloscope

It is recommended that you use the **Oscilloscope** software from [[oscilloscopemusic.com]]. *Shout out to the **Jerobeam Fenderson** guys for getting me in the oscilloscope drawing stuff!*

Use the VB-CABLE Virtual Audio Device to connect your software to the oscilloscope. Download it from here: [https://vb-audio.com/Cable/]

# Demos

You can run some demos from the `demos` folder. You may need to understand other concepts first.

# Gallery

*TODO*

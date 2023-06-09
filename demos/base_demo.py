import logging
from random import random
from time import localtime
from oscdraw.draw import Canvas
from oscdraw.objects import Point, Line, Ellipse, ObjectCollection
try:
    import keyboard
    keyboard_enabled = True
except:
    keyboard_enabled = False
    logging.warning("Optional dependency not found: \"keyboard\"; BasicTextTypewriter demo won't work.")


class Demo:
    """
    A demo. To run this demo, create a new instance of this class and run the run() function of it.
    Press Ctrl+C to exit.
    """
    def __init__(self, audio_device_index: int = None, rate: int = 192000):
        self.c = Canvas(audio_device_index, rate)

    def run(self):
        ...

class _Dev_BasicTextTypewriter(Demo):
    def key_pressed_hook(self, event):
        if event.event_type == keyboard.KEY_DOWN:
            self.text += event.name

    def run_main(self):
        if not keyboard_enabled:
            raise NotImplementedError("keyboard not found")
        CHR_WIDTH = 5000
        CHR_HEIGHT = 5000
        BOX_POS = 30000
        BOX_PADDING = 1000
        box = ObjectCollection(
            Line((-BOX_POS, BOX_POS, BOX_POS, BOX_POS)),
            Line((BOX_POS, BOX_POS, BOX_POS, -BOX_POS)),
            Line((BOX_POS, -BOX_POS, -BOX_POS, -BOX_POS)),
            Line((-BOX_POS, -BOX_POS, -BOX_POS, BOX_POS))
        )
        CHR_PER_LINE = (BOX_POS * 2 - BOX_PADDING * 2) // CHR_WIDTH
        self.text = ""
        keyboard.hook(self.key_pressed_hook, True)
        while True:
            if len(self.text) > 0:
                text = self.text
                lines = text.splitlines()
                i = 0
                while i < len(lines):
                    if len(lines[i]) > CHR_PER_LINE:
                        lines.insert(i, lines[i][:CHR_PER_LINE])
                        lines[i+1] = lines[i+1][CHR_PER_LINE:]
                    i += 1
                text = "\n".join(lines)
            self.c.draw_font("text", -BOX_POS + BOX_PADDING, BOX_POS - BOX_PADDING, 10000, 100,
                             "square", CHR_WIDTH, CHR_HEIGHT, 0, CHR_HEIGHT // 2)
            self.c.draw_font("text", -30000, 30000, 10000, 100, "square", 5000, 5000, 0, 2500)
            self.c.draw_object_collection(box, 10000, 10, "triangle")
            self.c.write()


    def run(self):
        try:
            self.run_main()
        except KeyboardInterrupt:
            keyboard.unhook()
            exit()


if __name__ == "__main__":
    logging.warning("This python file contains the Demo base class and WIP demos. Make sure to look for individual files and not run this one.")
from base_demo import *

class DigitalClock(Demo):
    def run(self):
        while True:
            t = localtime()
            hour = str(t.tm_hour).zfill(2)
            min_ = str(t.tm_min).zfill(2)
            sec = str(t.tm_sec).zfill(2)
            char_width, char_height = 8000, 10000
            self.c.draw_font(f"{hour}:{min_}:{sec}",
                             -(char_width * 8 / 2), char_height / 2, 5000, 10 / 8,
                             "triangle", char_width, char_height)
            self.c.write()
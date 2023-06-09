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

class BouncyBall(Demo):
    def _transform_ball(self, line: Line, ellipse_centre: Point, ellipse_size: int = 5000) -> Ellipse:
        if line.p1.x - ellipse_size / 2 < ellipse_centre.x < line.p2.x + ellipse_size / 2:
            y = (line.p1.y + line.p2.y) / 2
            y_dist = abs(ellipse_centre.y - y)
            ellipse = Ellipse(ellipse_centre,
                              height=ellipse_size if y_dist > ellipse_size / 2 else y_dist * 2,
                              width=ellipse_size if y_dist > ellipse_size / 2 else 1 / (y_dist * 2 / ellipse_size) * ellipse_size)
        else:
            ellipse = Ellipse(ellipse_centre, ellipse_size, ellipse_size)
        return ellipse

    def run(self):
        """
        This demo gets buggy after a while, so be sure to stop it.
        :return:
        """
        ground = Line((-27500, -22500, 27500, -22500))
        ball_c = Point(10000*random()-5000, 20000)
        ball_vel = Point(400*random()+100, 0)
        ball_size = 10000
        gravity = Point(0, -9.8)
        bounce_stiffness_percent = .75
        bounce_energy_percent = .99
        while True:
            ball_vel += gravity
            ball_c += ball_vel
            if ball_c.y <= (ground.p1.y + ground.p2.y) / 2 + (ball_size / 2 * bounce_stiffness_percent):
                ball_vel.y *= -bounce_energy_percent
            if not (ground.p1.x + ball_size / 2 < ball_c.x < ground.p2.x - ball_size / 2):
                ball_vel.x *= -bounce_energy_percent
            """if ground.p1.y + (ball_size / 2 * (bounce_stiffness_percent / (1 + bounce_energy_percent))) > ball_c.y:
                ball_c.y = ground.p1.y + (ball_size / 2 * (bounce_stiffness_percent / (1 + bounce_energy_percent)))"""
            ellipse = self._transform_ball(ground, ball_c, ball_size)
            self.c.draw_line(ground, 440, 10)
            self.c.draw_ellipse(ellipse, 440, 10)
            self.c.change_clip(-30000, 30000, 30000, -30000, False)
            self.c.write()


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
    #  BasicTextTypewriter(5).run()
    pass
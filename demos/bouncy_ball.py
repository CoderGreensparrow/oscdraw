from base_demo import *


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


if __name__ == '__main__':
    BouncyBall().run()
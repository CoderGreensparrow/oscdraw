from oscdraw.draw import *
from oscdraw.audioview import AudioPlotView
import keyboard
from random import random

c = Canvas(8)
#  a = AudioPlotView(c)

auto_player_left = True
auto_player_right = True

player_left_score = 0
player_right_score = 0
run = True
while run:
    ball = Point(0, 0)
    ball_vel = Point((-1 if random() < 0.5 else 1) * random()*250 + 750, random()*250 + 750)  # Yes, this is now a vector
    ball_height = 2000
    player_x = 24000
    player_left = Point(-player_x, 0)
    player_right = Point(player_x, 0)
    player_vel = 1000
    player_height = 15000
    walls_pos = 30000
    walls = Polygon((-walls_pos, walls_pos), (walls_pos, walls_pos), (walls_pos, -walls_pos), (-walls_pos, -walls_pos))
    round = True
    while round:
        """fps = m.measure()
        print(f"\r{fps*1000} FPS", end="")"""
        # collisions
        prev_vel = ball_vel
        ball_radius = ball_height / 2
        if walls_pos - ball_radius < abs(ball.x) < walls_pos + ball_radius:
            if ball.x < 0:
                player_right_score += 1
            else:
                player_left_score += 1
            round = False
        if player_x - ball_radius < abs(ball.x) < player_x + ball_radius:  # If x position could be in player
            if ball.x < 0 and player_left.y - player_height / 2 < ball.y < player_left.y + player_height / 2:  # if x and y position is in left player
                ball_vel.x *= -1
                # edge case
                if player_x - ball_radius < abs(
                        ball.x + ball_vel.x) < player_x + ball_radius:  # If would be still in player after moving (aka. on corner)
                    ball_vel.y *= -1
                    # Move too (twice actually)
                    ball += ball_vel
            elif ball.x > 0 and player_right.y - player_height / 2 < ball.y < player_right.y + player_height / 2:  # if x and y position is in right player
                ball_vel.x *= -1
                # edge case
                if player_x - ball_radius < abs(
                        ball.x + ball_vel.x) < player_x + ball_radius:  # If would be still in player after moving (aka. on corner)
                    ball_vel.y *= -1
                    # Move too (twice actually)
                    ball += ball_vel
        if walls_pos - ball_radius < abs(ball.y) < walls_pos + ball_radius:
            ball_vel.y *= -1
        # movement
        ball += ball_vel
        if not auto_player_left:
            if keyboard.is_pressed("w"): player_left.y += player_vel
            if keyboard.is_pressed("s"): player_left.y -= player_vel
        else:
            if player_left.y < ball.y: player_left.y += player_vel
            if player_left.y > ball.y: player_left.y -= player_vel
        if not auto_player_right:
            if keyboard.is_pressed("up"): player_right.y += player_vel
            if keyboard.is_pressed("down"): player_right.y -= player_vel
        else:
            if player_right.y < ball.y: player_right.y += player_vel
            if player_right.y > ball.y: player_right.y -= player_vel
        if player_left.y - player_height / 2 < -walls_pos: player_left.y = -walls_pos + player_height / 2
        if player_left.y + player_height / 2 > walls_pos: player_left.y = walls_pos - player_height / 2
        if player_right.y - player_height / 2 < -walls_pos: player_right.y = -walls_pos + player_height / 2
        if player_right.y + player_height / 2 > walls_pos: player_right.y = walls_pos - player_height / 2
        # draw
        c.draw_polygon(walls, 1000, 5)
        c.draw_ellipse((ball.x, ball.y, ball_height, ball_height), 440, 3)
        c.draw_line((player_left.x, player_left.y - player_height / 2,
                     player_left.x, player_left.y + player_height / 2), 440, 3)
        c.draw_line((player_right.x, player_right.y - player_height / 2,
                     player_right.x, player_right.y + player_height / 2), 440, 3)
        c.change_rotate((ball.x/35000)**3, Point(0, 0), False)
        c.change_shift((ball.x/3000)**3, (ball.y/3000)**3, False)
        #  c.change_clip(-2**15, 2**15-1, 2**15-1, -2**15, False)
        #  a.plot()
        c.write()
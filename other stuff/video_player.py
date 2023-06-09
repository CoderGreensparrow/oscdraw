import time
from moviepy.editor import VideoFileClip
import numpy as np
from oscdraw.draw import Canvas
from oscdraw.pixeldisplay import BWDisplay
import logging

def get_clip_size(video_file):
    clip = VideoFileClip(video_file)
    width, height = clip.size
    return width, height

def play_clip(pixeldisplay: BWDisplay, video_file, skip_pixels: int = 30, skip_lines: int = 3, size_multiply: float | int = 10):
    clip = VideoFileClip(video_file)
    width, height = clip.size
    clip_fps = clip.fps
    logging.info(f"{width}, {height}")
    skip_frame = 1
    start = time.perf_counter()
    for i, frame in enumerate(clip.iter_frames()):
        if i % skip_frame != 0:
            continue
        fps = 1 / (time.perf_counter() - start)
        start = time.perf_counter()
        skip_frame = clip_fps / fps
        if skip_frame < 1:
            time.sleep(1 / clip_fps - 1 / fps)
            skip_frame = 1
        else:
            skip_frame = round(skip_frame)
        rgb = frame.flatten()
        rgb = np.divide(rgb, 255)
        rgb = np.round(rgb)
        #  rgb = [rgb[i] for i in range(len(rgb)) if i % 3 == 0]
        pixeldisplay.update(rgb)
        pixeldisplay.draw(scale_x=size_multiply/3, scale_y=size_multiply, skip_pixels=skip_pixels, skip_lines=skip_lines)
        pixeldisplay.c.write()

def main():
    c = Canvas(5, record=False)
    video_file = input("FILE > ")
    size_multiply = float(input("SIZE MULTIPLY > "))
    b = BWDisplay(c, (get_clip_size(video_file)[0]*3, get_clip_size(video_file)[1]))
    play_clip(b, video_file, # get_clip_size(video_file)[0]//120,
              2, 2,
              size_multiply)
    #  c.audio.save()
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
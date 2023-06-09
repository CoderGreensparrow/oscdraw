from threading import Thread
from PIL import Image
import numpy as np
from oscdraw.draw import Canvas
from oscdraw.pixeldisplay import BWDisplay
import logging

def get_img_size(img_file):
    img = Image.open(img_file)
    width, height = img.size
    return width, height

def display_image(pixeldisplay: BWDisplay, img_file, skip_pixels: int = 30, skip_lines: int = 3, size_multiply: float | int = 10):
    img = Image.open(img_file)
    img = img.convert("RGB")
    width, height = img.size
    logging.info(f"{width}, {height}")
    rgb = np.asarray(img.getdata()).flatten()
    rgb = np.divide(rgb, 255)
    rgb = np.round(rgb)
    logging.debug("rgb set up")
    pixeldisplay.update(rgb)
    logging.debug("pixeldisplay updated")
    pixeldisplay.draw(scale_x=size_multiply/3, scale_y=size_multiply, skip_pixels=skip_pixels, skip_lines=skip_lines)
    logging.debug("drawn to memory")
    for i in range(1):
        pixeldisplay.c.write(clear=False)
    pixeldisplay.c.clear()

def main():
    c = Canvas(5)
    while True:
        img_file = input("FILE > ")
        size_multiply = float(input("SIZE MULTIPLY > "))
        b = BWDisplay(c, (get_img_size(img_file)[0]*3, get_img_size(img_file)[1]))
        display_image(b, img_file,  # get_clip_size(video_file)[0]//120,
                      0, 0,
                      size_multiply)
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
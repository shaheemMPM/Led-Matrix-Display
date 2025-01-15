#!/usr/bin/env python
import os

if os.environ.get("LED_MATRIX_ENV") == "development":
    from RGBMatrixEmulator import graphics
else:
    from rgbmatrix import graphics

from samplebase import SampleBase


class MyFirstDisplay(SampleBase):
    def __init__(self, *args, **kwargs):
        super(MyFirstDisplay, self).__init__(*args, **kwargs)

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("./fonts/7x13.bdf")
        textColor = graphics.Color(255, 0, 0)  # Red color

        while True:
            offscreen_canvas.Clear()
            graphics.DrawText(offscreen_canvas, font, 2, 32, textColor, "My First")
            graphics.DrawText(offscreen_canvas, font, 2, 48, textColor, "Display!")

            # Update the display
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)


if __name__ == "__main__":
    my_display = MyFirstDisplay()
    if not my_display.process():
        my_display.print_help()

#!/usr/bin/env python
import os
import time
from datetime import datetime

if os.environ.get("LED_MATRIX_ENV") == "development":
    from RGBMatrixEmulator import graphics
else:
    from rgbmatrix import graphics

from samplebase import SampleBase


class ClockDisplay(SampleBase):
    def __init__(self, *args, **kwargs):
        super(ClockDisplay, self).__init__(*args, **kwargs)
        self.parser.add_argument(
            "--title-color",
            type=str,
            help="Color for title text in R,G,B format",
            default="255,0,0",
        )  # Default red
        self.parser.add_argument(
            "--info-color",
            type=str,
            help="Color for date/time info in R,G,B format",
            default="0,255,0",
        )  # Default green

    def get_center_position(self, text, font):
        text_width = graphics.DrawText(
            self.matrix.CreateFrameCanvas(), font, 0, 0, graphics.Color(0, 0, 0), text
        )
        return max(0, (self.matrix.width - text_width) // 2)

    def draw_underline(self, canvas, x, y, width, color):
        for i in range(width):
            canvas.SetPixel(x + i, y, color.red, color.green, color.blue)

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("./fonts/7x13.bdf")

        # Parse colors
        title_rgb = [int(x) for x in self.args.title_color.split(",")]
        info_rgb = [int(x) for x in self.args.info_color.split(",")]
        title_color = graphics.Color(*title_rgb)
        info_color = graphics.Color(*info_rgb)

        # Vertical spacing
        line_height = 13  # Based on font size 7x13
        margin_left = 2
        title_text = "Astral"

        while True:
            offscreen_canvas.Clear()
            now = datetime.now()

            # Line 1: "Astral" centered
            title_x = self.get_center_position(title_text, font)
            title_y = line_height
            graphics.DrawText(
                offscreen_canvas, font, title_x, title_y, title_color, title_text
            )

            # Line 2: Underline
            title_width = graphics.DrawText(
                offscreen_canvas, font, 0, 0, title_color, title_text
            )
            self.draw_underline(
                offscreen_canvas, title_x, title_y + 2, title_width, title_color
            )

            # Line 3: Date (dd-mm-yyyy)
            date_str = now.strftime("%d-%m-%Y")
            graphics.DrawText(
                offscreen_canvas,
                font,
                margin_left,
                title_y + line_height + 8,
                info_color,
                date_str,
            )

            # Line 4: Day name
            day_str = now.strftime("%A")
            graphics.DrawText(
                offscreen_canvas,
                font,
                margin_left,
                title_y + 2 * line_height + 8,
                info_color,
                day_str,
            )

            # Line 5: Time with seconds (12-hour format)
            time_str = now.strftime("%I:%M:%S %p")
            graphics.DrawText(
                offscreen_canvas,
                font,
                margin_left,
                title_y + 3 * line_height + 8,
                info_color,
                time_str,
            )

            # Update display
            time.sleep(0.1)  # Small delay to prevent excessive updates
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)


if __name__ == "__main__":
    clock_display = ClockDisplay()
    if not clock_display.process():
        clock_display.print_help()

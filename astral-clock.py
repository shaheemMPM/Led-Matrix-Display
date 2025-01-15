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

    def get_center_position(self, text, font, dummy_canvas):
        # Use the provided canvas instead of creating a new one
        text_width = graphics.DrawText(
            dummy_canvas, font, 0, 0, graphics.Color(0, 0, 0), text
        )
        return max(0, (self.matrix.width - text_width) // 2)

    def draw_underline(self, canvas, x, y, width, color):
        for i in range(width):
            canvas.SetPixel(x + i, y, color.red, color.green, color.blue)

    def run(self):
        # Create canvases for double buffering
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        dummy_canvas = self.matrix.CreateFrameCanvas()  # For text width calculations

        # Main font for title and time
        main_font = graphics.Font()
        main_font.LoadFont("./fonts/7x13.bdf")

        # Smaller font for date and day
        small_font = graphics.Font()
        small_font.LoadFont("./fonts/6x10.bdf")

        # Parse colors
        title_rgb = [int(x) for x in self.args.title_color.split(",")]
        info_rgb = [int(x) for x in self.args.info_color.split(",")]
        title_color = graphics.Color(*title_rgb)
        info_color = graphics.Color(*info_rgb)

        # Vertical spacing
        main_line_height = 13  # Based on font size 7x13
        small_line_height = 10  # Based on font size 6x10
        margin_left = 2
        title_text = "Astral"

        # Pre-calculate title position and width (since it's static)
        title_x = self.get_center_position(title_text, main_font, dummy_canvas)
        title_width = graphics.DrawText(
            dummy_canvas, main_font, 0, 0, title_color, title_text
        )

        while True:
            offscreen_canvas.Clear()
            now = datetime.now()

            # Line 1: "Astral" centered
            title_y = main_line_height
            graphics.DrawText(
                offscreen_canvas, main_font, title_x, title_y, title_color, title_text
            )

            # Line 2: Underline
            self.draw_underline(
                offscreen_canvas, title_x, title_y + 2, title_width, title_color
            )

            # Line 3: Date (dd-mm-yyyy) with smaller font
            date_str = now.strftime("%d-%m-%Y")
            graphics.DrawText(
                offscreen_canvas,
                small_font,
                margin_left,
                title_y + main_line_height + 4,
                info_color,
                date_str,
            )

            # Line 4: Day name with smaller font
            day_str = now.strftime("%A")
            graphics.DrawText(
                offscreen_canvas,
                small_font,
                margin_left,
                title_y + main_line_height + small_line_height + 6,
                info_color,
                day_str,
            )

            # Line 5: Time with seconds (12-hour format)
            time_str = now.strftime("%I:%M:%S %p")
            graphics.DrawText(
                offscreen_canvas,
                main_font,
                margin_left,
                title_y + main_line_height + 2 * small_line_height + 14,
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

# Python LED Matrix Display Documentation

## Overview

This project provides a Python-based implementation for controlling RGB LED matrix displays using the Raspberry Pi. It's built on top of the rpi-rgb-led-matrix library but provides a more Python-friendly interface and includes an emulator for development without physical hardware.

## System Architecture

### Core Components

1. **Base Framework (`samplebase.py`)**

   - Provides the foundation class `SampleBase` for all LED matrix applications
   - Handles command-line argument parsing
   - Manages matrix initialization and configuration
   - Controls hardware interface setup

2. **Display Applications**

   - `run-text.py`: Scrolling text display
   - `pulsing-colors.py`: Color animation display
   - Extensible framework for creating new display patterns

3. **Hardware Abstraction**
   - Uses `RGBMatrix` and `RGBMatrixOptions` from rgbmatrix/RGBMatrixEmulator
   - Supports both physical LED matrices and emulated displays
   - Handles double-buffering for smooth animations

## Setup and Installation

1. **Dependencies**

```toml
dependencies = [
    "rgbmatrix",  # Hardware interface
    "rgbmatrixemulator>=0.11.6"  # Development/testing
]
```

2. **Installation**

```bash
# Install using uv package manager
uv install
```

3. **Font Requirements**
   - Uses BDF bitmap fonts
   - Default font: 7x13.bdf in fonts directory

## Creating Custom Displays

### Basic Structure

```python
from samplebase import SampleBase

class CustomDisplay(SampleBase):
    def __init__(self, *args, **kwargs):
        super(CustomDisplay, self).__init__(*args, **kwargs)
        # Add custom initialization here

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        while True:
            # Update display logic here
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
```

### Core Features Available

1. **Canvas Operations**

   - `CreateFrameCanvas()`: Create a new drawing surface
   - `SwapOnVSync()`: Update display with double buffering
   - `Fill(r, g, b)`: Fill entire canvas with color
   - `Clear()`: Clear the canvas

2. **Text Rendering**

```python
from RGBMatrixEmulator import graphics

font = graphics.Font()
font.LoadFont("path/to/font.bdf")
graphics.DrawText(canvas, font, x, y, color, text)
```

3. **Color Management**

```python
from RGBMatrixEmulator import graphics
color = graphics.Color(red, green, blue)  # Values 0-255
```

### Configuration Options

Key configuration parameters available through command line or code:

```python
options = RGBMatrixOptions()
options.rows = 32          # Display height
options.cols = 64          # Display width
options.chain_length = 1   # Number of daisy-chained panels
options.parallel = 1       # Number of parallel chains
options.brightness = 100   # Brightness (1-100)
options.hardware_mapping = 'regular'  # GPIO mapping
```

## Development and Testing

### Using the Emulator

The project includes an emulator configuration for development:

```json
{
  "pixel_size": 16,
  "display_adapter": "browser",
  "browser": {
    "port": 8888,
    "target_fps": 24,
    "quality": 70
  }
}
```

### Running Examples

```bash
# Run scrolling text
uv run run-text.py --text="Your Text Here"

# Run color animation
uv run pulsing-colors.py
```

## Converting Current C++ Clock to Python

To recreate the current clock implementation in Python:

```python
from samplebase import SampleBase
from RGBMatrixEmulator import graphics
import time
from datetime import datetime

class ClockDisplay(SampleBase):
    def __init__(self, *args, **kwargs):
        super(ClockDisplay, self).__init__(*args, **kwargs)

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("./fonts/7x13.bdf")
        text_color = graphics.Color(21, 245, 186)  # Custom color

        while True:
            offscreen_canvas.Clear()
            now = datetime.now()

            # Draw day name
            day = now.strftime("%A")
            graphics.DrawText(offscreen_canvas, font, 2, 12, text_color, day)

            # Draw time
            time_str = now.strftime("%I:%M:%S")
            graphics.DrawText(offscreen_canvas, font, 2, 25, text_color, time_str)

            # Update display
            time.sleep(0.1)  # Small delay to prevent excessive updates
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

if __name__ == "__main__":
    clock_display = ClockDisplay()
    if (not clock_display.process()):
        clock_display.print_help()
```

### Creating a Service

Create a systemd service file `/etc/systemd/system/led-clock-python.service`:

```ini
[Unit]
Description=LED Clock Python
After=network.target

[Service]
ExecStart=/path/to/python /path/to/clock_display.py --led-cols=64 --led-rows=64 --led-brightness=60 --led-slowdown-gpio=4
User=root
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl enable led-clock-python.service
sudo systemctl start led-clock-python.service
```

## Troubleshooting

Common issues and solutions:

1. **Display Not Updating**

   - Check GPIO permissions
   - Verify hardware configuration
   - Ensure proper power supply

2. **Performance Issues**

   - Adjust refresh rate in code
   - Optimize drawing operations
   - Check system load

3. **Text Display Problems**
   - Verify font file exists and is readable
   - Check text positioning
   - Ensure proper character encoding

## Best Practices

1. **Performance**

   - Use double buffering (SwapOnVSync)
   - Minimize drawing operations
   - Batch updates when possible

2. **Code Organization**

   - Inherit from SampleBase
   - Separate display logic from data processing
   - Use configuration files for settings

3. **Development**
   - Use emulator for initial development
   - Test with different screen sizes
   - Handle errors gracefully

# LED Matrix Clock System Documentation

## System Overview

The LED Matrix Clock is implemented as a systemd service on a Raspberry Pi that displays the current time on a 64x64 RGB LED matrix panel. The system consists of several key components:

1. Hardware Components:

   - Raspberry Pi (any model except Pi 5)
   - 64x64 RGB LED Matrix Panel
   - Power supply for the LED Matrix
   - GPIO connections between Pi and Matrix

2. Software Components:

   - rpi-rgb-led-matrix library
   - Custom systemd service (led-clock.service)
   - Clock application binary

3. Key Features:
   - Real-time clock display
   - Network time synchronization
   - Auto-start on boot
   - Configurable display parameters

## Hardware Configuration

The system uses a 64x64 RGB LED matrix with the following specifications:

- Resolution: 64x64 pixels
- Color: 24-bit RGB color (8 bits per channel)
- Interface: HUB75 connector
- Scan Rate: Standard 1/32 scan rate

The matrix is connected to the Raspberry Pi's GPIO pins according to the standard HUB75 pin mapping.

## Software Architecture

### Service Configuration

The system uses a systemd service for automatic startup and management:

Location: `/etc/systemd/system/led-clock.service`

Key Service Parameters:

- Starts after network connectivity
- Runs as root
- Automatic restart on failure
- Uses specific font and color settings

### Clock Application

The clock application is built from the rpi-rgb-led-matrix library's example code with the following features:

- Two-line display format
- First line: Full day name (Monday, Tuesday, etc.)
- Second line: Time in 12-hour format with seconds
- Custom color: rgb(21,245,186)
- Custom font: 7x13.bdf

### Network Time Synchronization

The system relies on network connectivity for accurate time:

1. Initial boot may show incorrect time
2. Connects to previously configured WiFi network
3. Synchronizes time using NTP
4. Updates display automatically when correct time is received

## User Configuration

Current configuration parameters in use:

- Display dimensions: 64x64 pixels
- Font: 7x13.bdf
- Text color: rgb(21,245,186)
- Display format: "%A" (day) and "%I:%M:%S" (time)
- Hardware options:
  - No hardware pulse
  - GPIO slowdown: 4
  - Brightness: 60%

These parameters can be modified by editing the systemd service file and restarting the service.

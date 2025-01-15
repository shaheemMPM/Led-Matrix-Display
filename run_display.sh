#!/bin/bash

# Detect the operating system
if [[ $(uname) == "Darwin" ]]; then
    # macOS (local development)
    echo "Running in development environment (macOS)..."
    LED_MATRIX_ENV=development python my_first_display.py --led-rows=64 --led-cols=64
elif [[ $(uname -m) =~ ^(arm|aarch64) ]]; then
    # Raspberry Pi (production)
    echo "Running in production environment (Raspberry Pi)..."
    
    # First stop the existing service
    sudo systemctl stop led-clock.service
    
    # Run with hardware settings
    sudo LED_MATRIX_ENV=production python my_first_display.py \
        --led-rows=64 \
        --led-cols=64 \
        --led-no-hardware-pulse \
        --led-slowdown-gpio=4 \
        --led-brightness=60
else
    echo "Unsupported environment"
    exit 1
fi
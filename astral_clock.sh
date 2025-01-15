#!/bin/bash

# Detect the operating system
if [[ $(uname) == "Darwin" ]]; then
    # macOS (local development)
    echo "Running in development environment (macOS)..."
    LED_MATRIX_ENV=development python astral-clock.py --led-rows=64 --led-cols=64
elif [[ $(uname -m) =~ ^(arm|aarch64) ]]; then
    # Raspberry Pi (production)
    echo "Running in production environment (Raspberry Pi)..."
    
    # Run with hardware settings
    sudo LED_MATRIX_ENV=production python astral-clock.py \
        --led-rows=64 \
        --led-cols=64 \
        --led-no-hardware-pulse true \
        --led-slowdown-gpio=4 \
        --led-brightness=60
else
    echo "Unsupported environment"
    exit 1
fi
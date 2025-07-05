#!/bin/bash

# P1 Reader Home Assistant Custom Component Installation Script
# This script helps install the P1 Reader custom component

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default Home Assistant config directory
DEFAULT_CONFIG_DIR="$HOME/.homeassistant"

echo -e "${GREEN}P1 Reader Home Assistant Custom Component Installer${NC}"
echo "=================================================="

# Check if Home Assistant config directory exists
if [ -z "$1" ]; then
    CONFIG_DIR="$DEFAULT_CONFIG_DIR"
else
    CONFIG_DIR="$1"
fi

if [ ! -d "$CONFIG_DIR" ]; then
    echo -e "${RED}Error: Home Assistant config directory not found at $CONFIG_DIR${NC}"
    echo "Usage: $0 [config_directory]"
    echo "Example: $0 /config  # For Home Assistant OS/Container"
    echo "Example: $0 ~/.homeassistant  # For Home Assistant Core"
    exit 1
fi

echo -e "${YELLOW}Installing to: $CONFIG_DIR${NC}"

# Create custom_components directory if it doesn't exist
CUSTOM_COMPONENTS_DIR="$CONFIG_DIR/custom_components"
if [ ! -d "$CUSTOM_COMPONENTS_DIR" ]; then
    echo "Creating custom_components directory..."
    mkdir -p "$CUSTOM_COMPONENTS_DIR"
fi

# Create p1_reader directory
P1_READER_DIR="$CUSTOM_COMPONENTS_DIR/p1_reader"
if [ -d "$P1_READER_DIR" ]; then
    echo -e "${YELLOW}P1 Reader directory already exists. Backing up...${NC}"
    mv "$P1_READER_DIR" "$P1_READER_DIR.backup.$(date +%Y%m%d_%H%M%S)"
fi

mkdir -p "$P1_READER_DIR"

# Copy component files
echo "Copying component files..."
cp custom_components/p1_reader/manifest.json "$P1_READER_DIR/"
cp custom_components/p1_reader/__init__.py "$P1_READER_DIR/"
cp custom_components/p1_reader/sensor.py "$P1_READER_DIR/"

# Set permissions
chmod 644 "$P1_READER_DIR"/*.py
chmod 644 "$P1_READER_DIR"/*.json

echo -e "${GREEN}Installation completed successfully!${NC}"
echo ""
echo "Next steps:"
echo "1. Add the following to your configuration.yaml:"
echo ""
echo "   sensor:"
echo "     - platform: p1_reader"
echo "       host: zap.local  # or your P1 Reader IP address"
echo ""
echo "2. Restart Home Assistant"
echo "3. Check the logs for any errors"
echo ""
echo "The component will create sensors for:"
echo "• Energy monitoring (import/export, power, reactive power)"
echo "• Device diagnostics (temperature, memory, WiFi status)"
echo "• System information (firmware version, uptime, device ID)"
echo ""
echo "For more configuration options, see the README.md file."
echo ""
echo -e "${YELLOW}Note: You may need to restart Home Assistant for the component to be recognized.${NC}" 
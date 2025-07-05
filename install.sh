#!/bin/bash

# Sourceful Energy Zap Home Assistant Custom Component Installation Script
# This script helps install the Sourceful Energy Zap custom component

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default Home Assistant config directory
DEFAULT_CONFIG_DIR="$HOME/.homeassistant"

echo -e "${GREEN}Sourceful Energy Zap Home Assistant Custom Component Installer${NC}"
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

# Create sourceful_zap directory
SOURCEFUL_ZAP_DIR="$CUSTOM_COMPONENTS_DIR/sourceful_zap"
if [ -d "$SOURCEFUL_ZAP_DIR" ]; then
    echo -e "${YELLOW}Sourceful Zap directory already exists. Backing up...${NC}"
    mv "$SOURCEFUL_ZAP_DIR" "$SOURCEFUL_ZAP_DIR.backup.$(date +%Y%m%d_%H%M%S)"
fi

mkdir -p "$SOURCEFUL_ZAP_DIR"

# Copy component files
echo "Copying component files..."
cp custom_components/sourceful_zap/manifest.json "$SOURCEFUL_ZAP_DIR/"
cp custom_components/sourceful_zap/__init__.py "$SOURCEFUL_ZAP_DIR/"
cp custom_components/sourceful_zap/sensor.py "$SOURCEFUL_ZAP_DIR/"

# Set permissions
chmod 644 "$SOURCEFUL_ZAP_DIR"/*.py
chmod 644 "$SOURCEFUL_ZAP_DIR"/*.json

echo -e "${GREEN}Installation completed successfully!${NC}"
echo ""
echo "Next steps:"
echo "1. Add the following to your configuration.yaml:"
echo ""
echo "   sensor:"
echo "     - platform: sourceful_zap"
echo "       host: zap.local  # or your Zap device IP address"
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
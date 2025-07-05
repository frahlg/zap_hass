# Sourceful Energy Zap Home Assistant Custom Component - Repository Structure

This document provides an overview of the complete repository structure and how to get started.

## Repository Structure

```
zap_hass/
├── README.md                           # Main documentation
├── LICENSE                             # MIT License
├── .gitignore                          # Git ignore rules
├── CHANGELOG.md                        # Version history
├── CONTRIBUTING.md                     # Development guidelines
├── hacs.json                           # HACS configuration
├── icon.png                            # Official Sourceful Energy logo
├── install.sh                          # Installation script
├── validate.py                         # Validation script
├── 
├── .github/
│   └── workflows/
│       └── validate.yml                # GitHub Actions CI
├── 
├── custom_components/
│   └── sourceful_zap/                  # Main component directory
│       ├── __init__.py                 # Component initialization
│       ├── manifest.json               # Component manifest
│       └── sensor.py                   # Sensor platform implementation
├── 
└── examples/
    └── configuration.yaml              # Configuration examples
```

## What's Included

### Core Component Files
- **`custom_components/sourceful_zap/`** - The main Home Assistant custom component
  - `__init__.py` - Component initialization and setup
  - `manifest.json` - Component metadata and requirements
  - `sensor.py` - Complete sensor platform with all OBIS codes

### Documentation
- **`README.md`** - Comprehensive documentation with installation and usage
- **`CONTRIBUTING.md`** - Guidelines for developers
- **`CHANGELOG.md`** - Version history and release notes
- **`REPOSITORY_STRUCTURE.md`** - This file

### Configuration & Examples
- **`examples/configuration.yaml`** - Complete configuration examples
- **`hacs.json`** - HACS (Home Assistant Community Store) configuration

### Development & Automation
- **`.github/workflows/validate.yml`** - GitHub Actions for continuous integration
- **`validate.py`** - Local validation script
- **`install.sh`** - Automated installation script

### Project Files
- **`LICENSE`** - MIT License
- **`.gitignore`** - Git ignore rules for Python and Home Assistant

## Quick Start

### 1. Manual Installation
```bash
# Clone the repository
git clone https://github.com/fredde/zap_hass.git
cd zap_hass

# Run the installation script
./install.sh

# Or manually copy files to your Home Assistant config directory
cp -r custom_components/p1_reader ~/.homeassistant/custom_components/
```

### 2. Configuration
Add to your `configuration.yaml`:
```yaml
sensor:
  - platform: p1_reader
    host: zap.local  # Your P1 Reader IP or hostname
```

### 3. Restart Home Assistant
Restart Home Assistant to load the new component.

## Supported Sensors

The component automatically creates sensors for all supported OBIS codes:

### Energy Sensors
- Total Energy Import/Export (kWh)
- Current Power Import/Export (kW)
- Net Power (calculated: import - export)

### Per-Phase Sensors
- Voltage L1/L2/L3 (V)
- Current L1/L2/L3 (A)
- Power Import/Export per phase (kW)

### Reactive Power Sensors
- Total Reactive Energy Import/Export (kVArh)
- Current Reactive Power Import/Export (kVAr)
- Reactive Power Import/Export per phase (kVAr)

### System & Device Sensors
- Device ID, Firmware Version, Uptime
- Temperature, Memory Usage (%, MB)
- CPU Frequency, Flash Size
- WiFi Status, SSID, Signal Strength
- Local IP Address

## Development

### Validation
Run the validation script to check everything is set up correctly:
```bash
python validate.py
```

### Contributing
See `CONTRIBUTING.md` for development guidelines.

### Testing
The component includes:
- GitHub Actions CI/CD pipeline
- Code formatting with Black
- Linting with flake8 and pylint
- Type checking with mypy
- Security scanning with bandit

## HACS Installation

This component is configured for HACS (Home Assistant Community Store):

1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click "Custom repositories"
4. Add this repository URL
5. Install the Sourceful Energy Zap integration

## API Compatibility

The component is designed to work with the [Sourceful Energy Zap](https://sourceful.energy/store/sourceful-energy-zap) P1 Reader API:

**Endpoint**: `http://zap.local/api/data/p1/obis`

**Expected Response Format**:
```json
{
  "status": "success",
  "ts": 1751722190484,
  "data": [
    "0-0:1.0.0(250705142950W)",
    "1-0:1.8.0(00061825.061*kWh)",
    "1-0:2.8.0(00008702.210*kWh)",
    "1-0:3.8.0(00000259.153*kVArh)",
    "1-0:4.8.0(00009399.569*kVArh)",
    "1-0:1.7.0(0000.000*kW)",
    "1-0:2.7.0(0000.385*kW)",
    "1-0:32.7.0(231.2*V)",
    "1-0:52.7.0(235.4*V)",
    "1-0:72.7.0(235.9*V)",
    "1-0:31.7.0(001.5*A)",
    "1-0:51.7.0(-001.2*A)",
    "1-0:71.7.0(-001.5*A)",
    ...
  ]
}
```

**Device Information:**
- Made by [Sourceful Labs AB](https://sourceful.energy) in Kalmar, Sweden 🇸🇪
- Compatible with standard P1 RJ12 smart meters across Europe
- No external power required - draws power from the smart meter
- Simple WiFi setup with no technical knowledge required

## Home Assistant Compatibility

- **Minimum Version**: Home Assistant 2023.1.0
- **Python Version**: 3.9+
- **Dependencies**: No external dependencies (uses built-in Home Assistant modules)

## License

This project is licensed under the MIT License. See `LICENSE` for details.

## Support

- **Issues**: Report bugs via GitHub Issues
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: See `README.md` for detailed documentation 
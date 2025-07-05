# P1 Reader Home Assistant Custom Component

A custom component for Home Assistant that integrates with the [Sourceful Energy Zap](https://sourceful.energy/store/sourceful-energy-zap) P1 Reader to monitor smart meter data.

The Sourceful Energy Zap is a P1 meter reader that gives you unprecedented clarity of your energy consumption to help reduce your bills. Made by [Sourceful Labs AB](https://sourceful.energy) in Kalmar, Sweden 🇸🇪, it's designed for European smart meters with standard P1 RJ12 ports.

## Features

- **Real-time monitoring** of P1 smart meter data from your Sourceful Energy Zap
- **Energy tracking** for both import and export
- **Per-phase monitoring** (L1, L2, L3) for voltage, current, and power
- **Reactive power monitoring** for comprehensive energy analysis
- **Net power calculation** (import - export)
- **Energy Dashboard integration** for Home Assistant's built-in energy management
- **Automatic device discovery** and sensor creation
- **No external power required** - the Zap draws power directly from your smart meter

## Supported Sensors

### Main Energy Sensors
- Total Energy Import (kWh)
- Total Energy Export (kWh)
- Current Power Import (kW)
- Current Power Export (kW)
- Net Power (kW) - calculated sensor

### Per-Phase Sensors
- Voltage L1/L2/L3 (V)
- Current L1/L2/L3 (A)
- Power Import/Export per phase (kW)

### Reactive Power Sensors
- Total Reactive Energy Import (kVArh)
- Total Reactive Energy Export (kVArh)
- Reactive Power per phase (kVAr)

### System & Device Sensors
- Device ID - unique identifier of your Zap device
- Firmware Version - current firmware version
- Uptime - how long the device has been running (seconds)
- Temperature - internal device temperature (°C)
- Memory Usage - RAM usage percentage and absolute values (MB)
- CPU Frequency - processor speed (MHz)
- Flash Size - storage capacity (MB)
- WiFi Status - connection status
- WiFi SSID - connected network name
- WiFi Signal Strength - signal strength (dBm)
- Local IP Address - device IP on your network

## Prerequisites

### Sourceful Energy Zap Device
You need a [Sourceful Energy Zap](https://sourceful.energy/store/sourceful-energy-zap) P1 meter reader connected to your smart meter.

### Meter Compatibility
The Sourceful Energy Zap is compatible with standard P1 RJ12 smart meters in European countries. For full compatibility details, check the [official compatibility guide](https://intercom.help/sourceful-energy/en/articles/11486814-which-meters-are-compatible-with-zap).

**Supported Countries:**
🇦🇹 Austria* | 🇧🇪 Belgium | 🇩🇰 Denmark | 🇫🇮 Finland | 🇭🇺 Hungary | 🇮🇪 Ireland
🇱🇹 Lithuania | 🇱🇺 Luxembourg | 🇳🇱 Netherlands | 🇵🇹 Portugal | 🇸🇪 Sweden

*Work in progress to support encrypted data

### Setup Requirements
- Sourceful Energy Zap connected to your smart meter's P1 port
- Zap connected to your WiFi network
- Zap accessible on your local network (default hostname: `zap.local`)

## Installation

### Method 1: Manual Installation

1. Download this repository
2. Copy the `custom_components/p1_reader` folder to your Home Assistant `custom_components` directory
3. Restart Home Assistant
4. Add the configuration to your `configuration.yaml`

### Method 2: HACS (Home Assistant Community Store)

1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL and select "Integration" as the category
6. Install the integration
7. Restart Home Assistant

## Configuration

Add the following to your `configuration.yaml`:

```yaml
sensor:
  - platform: p1_reader
    host: zap.local  # IP address or hostname of your P1 Reader
    endpoint: /api/data/p1/obis  # P1 data API endpoint (default)
    system_endpoint: /  # System info API endpoint (default)
    name: P1 Reader  # Optional: custom name prefix
    scan_interval: 10  # Optional: update interval in seconds (default: 10)
```

### Configuration Options

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `host` | Yes | `zap.local` | IP address or hostname of your P1 Reader |
| `endpoint` | No | `/api/data/p1/obis` | P1 data API endpoint path |
| `system_endpoint` | No | `/` | System information API endpoint path |
| `name` | No | `P1 Reader` | Custom name prefix for sensors |
| `scan_interval` | No | `10` | Update interval in seconds |

## Energy Dashboard Integration

To use with Home Assistant's Energy Dashboard:

1. Go to **Configuration** → **Energy**
2. Under **Grid consumption**, add: `sensor.p1_reader_total_energy_import`
3. Under **Return to grid**, add: `sensor.p1_reader_total_energy_export`
4. Save the configuration

## API Data Format

The component connects to your Sourceful Energy Zap via two local API endpoints:

### P1 Energy Data
**API Endpoint:** `http://zap.local/api/data/p1/obis` (or use your Zap's IP address)

**Response Format:**
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

The component automatically parses all OBIS codes from the data array and creates corresponding Home Assistant sensors.

### System Information Data
**API Endpoint:** `http://zap.local/` (or use your Zap's IP address)

**Response Format:**
```json
{
  "time_utc_sec": 1751723323,
  "uptime_seconds": 86569,
  "temperature_celsius": 31.1856,
  "memory_MB": {
    "total": 0.27689,
    "available": 0.0648079,
    "free": 0.0648079,
    "used": 0.212082,
    "percent_used": 76.5943
  },
  "zap": {
    "deviceId": "zap-0000e421347506dc",
    "cpuFreqMHz": 160,
    "flashSizeMB": 4,
    "sdkVersion": "4.4.5.230722",
    "firmwareVersion": "0.1.4",
    "network": {
      "wifiStatus": "connected",
      "localIP": "192.168.1.235",
      "ssid": "your-wifi-network",
      "rssi": -49
    }
  }
}
```

The component extracts system information and creates diagnostic sensors for device monitoring and troubleshooting.

## Troubleshooting

### Common Issues

1. **No sensors appearing**: 
   - Check that the Sourceful Energy Zap is accessible at the configured host
   - Verify the Zap is connected to your WiFi network
   - Try accessing `http://zap.local/api/data/p1/obis` in a browser

2. **Connection errors**: 
   - Ensure the Zap is on the same network as Home Assistant
   - If using IP address instead of hostname, verify the correct IP
   - Check that the P1 port on your smart meter is properly connected

3. **Sensor values not updating**: 
   - Check Home Assistant logs for any error messages
   - Verify your smart meter is [compatible](https://intercom.help/sourceful-energy/en/articles/11486814-which-meters-are-compatible-with-zap)
   - Ensure the Zap has a solid connection to your smart meter's P1 port

### Zap Device Setup

If you're having trouble with the Sourceful Energy Zap device itself:

1. **Check the connection**: Ensure the Zap is properly connected to your smart meter's P1 port (RJ12)
2. **WiFi setup**: Make sure the Zap is connected to your WiFi network
3. **Power**: The Zap draws power from the smart meter - no external power needed
4. **Meter compatibility**: Verify your meter is supported using the [official compatibility guide](https://intercom.help/sourceful-energy/en/articles/11486814-which-meters-are-compatible-with-zap)

### Network Discovery

If `zap.local` doesn't work, try:
- Finding the Zap's IP address in your router's device list
- Using network scanning tools to find the device
- Checking your router's DHCP client list for "Sourceful" or "Zap"

### Logging

To enable debug logging, add this to your `configuration.yaml`:

```yaml
logger:
  logs:
    custom_components.p1_reader: debug
```

### Checking Logs

View logs in Home Assistant:
1. Go to **Configuration** → **Logs**
2. Search for "p1_reader"

Or check the log file directly:
```bash
grep p1_reader home-assistant.log
```

## Development

### Prerequisites

- Home Assistant development environment
- Python 3.9+
- Access to a P1 Reader device
- Docker (for local validation)

### Local Validation

Before pushing changes, you can run local validation to match the GitHub Actions environment:

```bash
./validate_local.sh
```

This script uses Docker to run the same checks as the CI pipeline:
- Black code formatting
- Python syntax validation  
- JSON file validation

### Code Formatting

The project uses Black for code formatting. To format your code:

```bash
# Using Docker (matches CI environment)
docker run --rm -v $(pwd):/app -w /app python:3.10-slim bash -c "pip install black && python -m black custom_components/"

# Or if you have Black installed locally
python -m black custom_components/
```

### Testing

1. Clone this repository
2. Set up a Home Assistant development environment
3. Install the component in development mode
4. Configure with your P1 Reader details
5. Test functionality and sensor updates

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: Please report bugs and feature requests through GitHub Issues
- **Discussions**: Use GitHub Discussions for general questions and community support

## Credits

- Developed for the [Sourceful Energy Zap](https://sourceful.energy/store/sourceful-energy-zap) P1 Reader
- Sourceful Energy Zap is a product of [Sourceful Labs AB](https://sourceful.energy), Kalmar, Sweden 🇸🇪
- Based on the OBIS (Object Identification System) standard for smart meter data
- Built for Home Assistant integration
- This integration is independently developed and not officially affiliated with Sourceful Labs AB

## Version History

- **1.0.0**: Initial release with basic P1 Reader support
- Support for all standard OBIS codes
- Energy Dashboard integration
- Per-phase monitoring capabilities 
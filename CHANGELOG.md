# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- System and device monitoring sensors
- Real device ID and firmware version in Home Assistant device registry
- Temperature monitoring sensor
- Memory usage sensors (total, used, free, percentage)
- Network status sensors (WiFi status, SSID, signal strength, local IP)
- Device information sensors (CPU frequency, flash size, SDK version)
- Uptime sensor for device health monitoring

### Changed
- Device information now uses real device ID from Zap instead of static identifier
- Firmware version is now retrieved from device and displayed in Home Assistant
- Configuration now supports separate endpoints for P1 data and system information

### Fixed
- Nothing yet

## [1.0.0] - 2025-01-05

### Added
- Initial release of P1 Reader Home Assistant Custom Component
- Support for [Sourceful Energy Zap](https://sourceful.energy/store/sourceful-energy-zap) P1 Reader API
- Automatic sensor creation for all standard OBIS codes
- Support for European smart meters with standard P1 RJ12 ports
- Energy sensors:
  - Total Energy Import/Export (kWh)
  - Current Power Import/Export (kW)
  - Total Reactive Energy Import/Export (kVArh)
  - Current Reactive Power Import/Export (kVAr)
- Per-phase monitoring:
  - Voltage L1/L2/L3 (V)
  - Current L1/L2/L3 (A)
  - Power Import/Export per phase (kW)
  - Reactive Power Import/Export per phase (kVAr)
- Calculated Net Power sensor (import - export)
- Home Assistant Energy Dashboard integration
- Proper device information and unique IDs
- Configurable scan interval and endpoint
- Comprehensive error handling and logging
- HACS (Home Assistant Community Store) support
- Example configurations and automation examples

### Technical Details
- Built for Home Assistant 2023.1.0 and newer
- Uses async/await for non-blocking API calls
- Implements proper throttling to avoid API spam
- Follows Home Assistant sensor entity guidelines
- Supports both IP address and hostname configuration
- Includes proper device class and state class assignments
- Regular expression parsing of OBIS codes
- Robust error handling for network and API issues

### Documentation
- Comprehensive README with installation instructions
- Configuration examples with all options
- Troubleshooting guide
- Contributing guidelines
- MIT License 
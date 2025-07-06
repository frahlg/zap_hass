# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Target: v1.0.0 - Home Assistant Core Submission
- [ ] Config flow implementation (UI configuration)
- [ ] Multi-device support
- [ ] Test coverage (80%+)
- [ ] DataUpdateCoordinator migration
- [ ] Quality scale requirements (diagnostics, logging, repairs)

## [0.1.0] - 2024-01-XX - Reference Implementation

### 🚀 Reference Implementation Status
This release marks the transition to a **community-driven reference implementation** seeking Home Assistant core inclusion.

### Added
- **Reference Implementation Status**: This is now a community-driven reference implementation seeking Home Assistant core inclusion
- Complete OBIS code sensor support (25+ energy sensors)
- System diagnostics sensors (12 system sensors)
- Dual API endpoint support (`/api/data/p1/obis` and `/api/system`)
- Energy Dashboard integration
- Per-phase monitoring (L1/L2/L3)
- Net power calculation
- HACS compatibility
- Official Sourceful Energy branding with authentic logo
- Comprehensive documentation and examples
- CI/CD pipeline with code quality checks (Black, flake8, pylint, mypy)
- Local validation script for efficient development

### Technical Implementation
- Basic YAML configuration (to be migrated to config flow)
- Single device support (to be expanded)
- Manual polling (to be migrated to DataUpdateCoordinator)
- No tests (critical for core inclusion)
- 35+ sensors total (25+ energy + 12 system)

### Energy Sensors
- Total Energy Import/Export (kWh)
- Current Power Import/Export (kW)
- Total Reactive Energy Import/Export (kVArh)
- Current Reactive Power Import/Export (kVAr)
- Per-phase monitoring (Voltage L1/L2/L3, Current L1/L2/L3, Power per phase)
- Calculated Net Power sensor (import - export)

### System Sensors
- Device ID and firmware version
- Temperature monitoring
- Memory usage (total, used, free, percentage)
- Network status (WiFi status, SSID, signal strength, local IP)
- Device information (CPU frequency, flash size, SDK version)
- Uptime sensor for device health monitoring

### Community Contributions Welcome
- See [Contributing & Earning Grants](README.md#contributing--earning-grants)
- Check [GitHub Issues](https://github.com/srcfl/spark-zap-home-assistant/issues) for available tasks
- Earn grants through [Spark Initiative](https://sourceful.energy/grants)

### Breaking Changes
- Repository renamed from `p1_reader` to `sourceful_zap`
- Configuration platform changed from `p1_reader` to `sourceful_zap`
- Component domain changed from `p1_reader` to `sourceful_zap`
- Default name changed from "P1 Reader" to "Zap"
- System endpoint corrected from "/" to "/api/system"

## Previous Development History

### Pre-0.1.0 - Development Phase
- Initial P1 reader implementation
- Basic OBIS code parsing
- Single device polling
- YAML configuration only
- No automated testing
- Development iterations and bug fixes
- Official Sourceful Energy product integration
- Real device information retrieval
- Comprehensive sensor suite development 
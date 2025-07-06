---
name: Multi-Device Support
about: Support multiple Zap devices in a single Home Assistant installation
title: "[MULTI-DEVICE] Support Multiple Zap Devices"
labels: ["enhancement", "multi-device", "ha-core-required"]
assignees: []
---

## 🎯 Goal
Implement support for multiple Sourceful Energy Zap devices in a single Home Assistant installation, enabling users with multiple smart meters or locations to monitor all devices.

## 📋 Requirements

### 1. Device Management
- [ ] Support multiple device entries through config flow
- [ ] Each device gets unique device ID and name
- [ ] Proper device registry management
- [ ] Device-specific configuration (different IP addresses, scan intervals)

### 2. Entity Naming
- [ ] Unique entity IDs per device to avoid conflicts
- [ ] Device-specific entity naming (e.g., "Zap Kitchen", "Zap Garage")
- [ ] Maintain backward compatibility with single device setups
- [ ] Clear entity naming convention

### 3. Data Coordinators
- [ ] Separate coordinator instance per device
- [ ] Independent update intervals per device
- [ ] Proper coordinator lifecycle management
- [ ] Error handling per device (one device failure doesn't affect others)

### 4. Configuration Management
- [ ] Multiple config entries support
- [ ] Device-specific options (scan interval, endpoints)
- [ ] Proper config entry cleanup on device removal
- [ ] Config validation per device

## 🔧 Technical Details

### Device Registry Integration
```python
# Each device should have unique identifiers
device_info = {
    "identifiers": {(DOMAIN, f"{device_id}_{config_entry.entry_id}")},
    "name": config_entry.data.get("name", "Zap"),
    "manufacturer": "Sourceful Labs AB",
    "model": "Sourceful Energy Zap",
    "sw_version": firmware_version,
    "configuration_url": f"http://{host}",
}
```

### Entity Naming Convention
- Single device: `sensor.zap_total_energy_import`
- Multiple devices: `sensor.zap_kitchen_total_energy_import`
- Use device name as prefix when multiple devices exist

### Coordinator Management
```python
class SourcefulZapCoordinator(DataUpdateCoordinator):
    """Data update coordinator for a single Zap device."""
    
    def __init__(self, hass, config_entry):
        self.config_entry = config_entry
        self.device_id = config_entry.data["device_id"]
        # Device-specific setup
```

## 📚 References
- [Home Assistant Device Registry](https://developers.home-assistant.io/docs/device_registry_index)
- [Config Entries](https://developers.home-assistant.io/docs/config_entries_index)
- [Multiple Device Examples](https://github.com/home-assistant/core/tree/dev/homeassistant/components)

## 🧪 Testing Requirements
- [ ] Test adding multiple devices
- [ ] Test device removal
- [ ] Test entity naming uniqueness
- [ ] Test independent device operation
- [ ] Test error handling per device

## 💰 Grant Opportunity
This task is eligible for grants through the [Sourceful Energy Spark Initiative](https://sourceful.energy/grants).

## 🚀 Getting Started
1. Comment below to claim this issue
2. Fork the repository
3. Create feature branch: `git checkout -b feature/multi-device-support`
4. Implement multi-device support
5. Add comprehensive tests
6. Submit PR with documentation updates

## ✅ Definition of Done
- [ ] Multiple devices can be added via config flow
- [ ] Each device has unique entity names
- [ ] Independent operation of each device
- [ ] Proper device cleanup on removal
- [ ] Tests cover multi-device scenarios
- [ ] Documentation updated with multi-device setup
- [ ] Backward compatibility maintained 
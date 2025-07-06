---
name: Config Flow Implementation
about: Implement UI configuration to replace YAML setup (Critical for HA Core)
title: "[CONFIG FLOW] Implement UI Configuration"
labels: ["enhancement", "config-flow", "ha-core-required", "good first issue"]
assignees: []
---

## 🎯 Goal
Implement Home Assistant config flow to replace YAML configuration, making the integration compatible with Home Assistant core requirements.

## 📋 Requirements

### 1. Config Flow Handler
- [ ] Create `config_flow.py` with `ConfigFlow` class
- [ ] Implement `async_step_user()` for manual configuration
- [ ] Add device discovery via mDNS/SSDP (if supported by Zap)
- [ ] Implement config validation and error handling
- [ ] Support both IP address and hostname input

### 2. Options Flow
- [ ] Create `OptionsFlow` class for configuration updates
- [ ] Allow changing scan interval
- [ ] Allow changing endpoint URLs
- [ ] Support device name customization

### 3. Configuration Schema
- [ ] Define config schema with appropriate validators
- [ ] Set sensible defaults (scan_interval: 30s, name: "Zap")
- [ ] Add input validation for IP/hostname and ports

### 4. Migration Support
- [ ] Detect existing YAML configuration
- [ ] Provide migration path or clear instructions
- [ ] Update documentation with new setup process

## 🔧 Technical Details

### Config Flow Structure
```python
class SourcefulZapConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Sourceful Zap."""
    
    VERSION = 1
    
    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        # Implementation here
        
    async def async_step_discovery(self, discovery_info):
        """Handle discovery step."""
        # Implementation here
```

### Required Fields
- `host` (IP address or hostname)
- `name` (device name, default: "Zap")
- `scan_interval` (seconds, default: 30)
- `p1_endpoint` (default: "/api/data/p1/obis")
- `system_endpoint` (default: "/api/system")

## 📚 References
- [Home Assistant Config Flow Documentation](https://developers.home-assistant.io/docs/config_entries_config_flow_handler)
- [Config Flow Examples](https://github.com/home-assistant/core/tree/dev/homeassistant/components)
- [Integration Quality Scale](https://developers.home-assistant.io/docs/integration_quality_scale_index)

## 💰 Grant Opportunity
This task is eligible for grants through the [Sourceful Energy Spark Initiative](https://sourceful.energy/grants).

## 🚀 Getting Started
1. Comment below to claim this issue
2. Fork the repository
3. Create feature branch: `git checkout -b feature/config-flow`
4. Implement config flow following HA guidelines
5. Add tests for the config flow
6. Submit PR with documentation updates

## ✅ Definition of Done
- [ ] Config flow implementation complete
- [ ] YAML configuration removed from examples
- [ ] Tests added for config flow
- [ ] Documentation updated
- [ ] Integration can be set up via UI only
- [ ] Existing users have clear migration path 
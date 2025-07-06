---
name: DataUpdateCoordinator Migration
about: Migrate to official DataUpdateCoordinator pattern for better error handling
title: "[COORDINATOR] Migrate to DataUpdateCoordinator Pattern"
labels: ["enhancement", "coordinator", "ha-core-required"]
assignees: []
---

## 🎯 Goal
Migrate from the current custom polling implementation to Home Assistant's official `DataUpdateCoordinator` pattern for better error handling, connection state management, and integration with Home Assistant core.

## 📋 Requirements

### 1. DataUpdateCoordinator Implementation
- [ ] Create `P1DataUpdateCoordinator` class extending `DataUpdateCoordinator`
- [ ] Create `SystemDataUpdateCoordinator` class extending `DataUpdateCoordinator`
- [ ] Implement proper async data fetching
- [ ] Add connection state management
- [ ] Implement proper error handling and retry logic

### 2. Sensor Integration
- [ ] Update all sensors to use `CoordinatorEntity`
- [ ] Implement `coordinator_context` for efficient updates
- [ ] Add proper availability handling
- [ ] Implement entity state management

### 3. Error Handling
- [ ] Implement exponential backoff for failed requests
- [ ] Add connection state tracking
- [ ] Handle network timeouts gracefully
- [ ] Implement proper logging for debugging
- [ ] Add repair suggestions for common issues

### 4. Configuration Management
- [ ] Support dynamic scan interval updates
- [ ] Implement coordinator refresh on config changes
- [ ] Add manual refresh capabilities
- [ ] Proper coordinator lifecycle management

## 🔧 Technical Details

### DataUpdateCoordinator Structure
```python
class P1DataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching P1 data from the API."""

    def __init__(self, hass, config_entry):
        """Initialize the coordinator."""
        self.config_entry = config_entry
        self.host = config_entry.data["host"]
        self.p1_endpoint = config_entry.data.get("p1_endpoint", "/api/data/p1/obis")
        
        update_interval = timedelta(seconds=config_entry.data.get("scan_interval", 30))
        
        super().__init__(
            hass,
            logger,
            name="P1 Data",
            update_interval=update_interval,
        )

    async def _async_update_data(self):
        """Fetch data from API endpoint."""
        try:
            async with async_timeout.timeout(10):
                # Fetch P1 data
                return await self._fetch_p1_data()
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")
```

### Sensor Integration
```python
class P1Sensor(CoordinatorEntity, SensorEntity):
    """Representation of a P1 sensor."""

    def __init__(self, coordinator, config_entry, obis_code, sensor_config):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.config_entry = config_entry
        self.obis_code = obis_code
        self.sensor_config = sensor_config

    @property
    def available(self):
        """Return True if coordinator is available."""
        return self.coordinator.last_update_success

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get(self.obis_code)
```

### Error Handling Features
- [ ] Exponential backoff (1s, 2s, 4s, 8s, 16s, 30s max)
- [ ] Connection state tracking (`connected`, `connecting`, `disconnected`)
- [ ] Detailed error messages and repair suggestions
- [ ] Graceful degradation when one API endpoint fails

## 📚 References
- [DataUpdateCoordinator Documentation](https://developers.home-assistant.io/docs/integration_fetching_data)
- [CoordinatorEntity Documentation](https://developers.home-assistant.io/docs/integration_fetching_data#coordinatorentity)
- [Error Handling Best Practices](https://developers.home-assistant.io/docs/integration_fetching_data#error-handling)

## 🧪 Testing Requirements
- [ ] Test coordinator initialization
- [ ] Test data fetching success scenarios
- [ ] Test error handling and recovery
- [ ] Test sensor availability states
- [ ] Test coordinator updates
- [ ] Test configuration changes
- [ ] Test manual refresh

## 💰 Grant Opportunity
This task is eligible for grants through the [Sourceful Energy Spark Initiative](https://sourceful.energy/grants).

## 🚀 Getting Started
1. Comment below to claim this issue
2. Fork the repository
3. Create feature branch: `git checkout -b feature/data-coordinator`
4. Implement DataUpdateCoordinator classes
5. Update sensors to use CoordinatorEntity
6. Add comprehensive tests
7. Submit PR with documentation

## ✅ Definition of Done
- [ ] DataUpdateCoordinator implemented for both P1 and system data
- [ ] All sensors use CoordinatorEntity
- [ ] Proper error handling and retry logic
- [ ] Connection state management
- [ ] Tests cover coordinator functionality
- [ ] Documentation updated
- [ ] Performance improved compared to current implementation
- [ ] Repair suggestions implemented 
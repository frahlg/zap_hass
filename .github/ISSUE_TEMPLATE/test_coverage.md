---
name: Test Coverage (80%+)
about: Add comprehensive pytest tests to meet HA core requirements
title: "[TESTS] Implement Comprehensive Test Coverage"
labels: ["testing", "ha-core-required", "good first issue"]
assignees: []
---

## 🎯 Goal
Implement comprehensive test coverage (80%+) using pytest to meet Home Assistant core requirements. Tests should cover all sensor types, API interactions, error conditions, and edge cases.

## 📋 Requirements

### 1. Test Structure
- [ ] Set up `tests/` directory with proper structure
- [ ] Create `conftest.py` with fixtures and mocks
- [ ] Implement `test_init.py` for component initialization
- [ ] Add `test_sensor.py` for sensor functionality
- [ ] Add `test_config_flow.py` for config flow (when implemented)

### 2. Mock API Responses
- [ ] Mock P1 API responses (`/api/data/p1/obis`)
- [ ] Mock system API responses (`/api/system`)
- [ ] Mock network error scenarios
- [ ] Mock timeout scenarios
- [ ] Mock malformed JSON responses

### 3. Sensor Testing
- [ ] Test all 25+ energy sensors
- [ ] Test all 12 system sensors
- [ ] Test sensor state calculations
- [ ] Test sensor attributes and device classes
- [ ] Test entity naming and unique IDs

### 4. Error Handling
- [ ] Test API connection failures
- [ ] Test invalid API responses
- [ ] Test timeout handling
- [ ] Test sensor unavailable states
- [ ] Test recovery from errors

### 5. Integration Testing
- [ ] Test component setup/teardown
- [ ] Test coordinator updates
- [ ] Test device information
- [ ] Test Energy Dashboard integration
- [ ] Test configuration validation

## 🔧 Technical Details

### Test Structure
```
tests/
├── conftest.py              # Fixtures and mocks
├── test_init.py            # Component initialization
├── test_sensor.py          # Sensor functionality
├── test_config_flow.py     # Config flow (future)
├── fixtures/
│   ├── p1_response.json    # Mock P1 API response
│   └── system_response.json # Mock system API response
└── __init__.py
```

### Mock Fixtures
```python
@pytest.fixture
def mock_p1_response():
    """Mock P1 API response."""
    return {
        "1.0.0": "1234567890123456",
        "1.8.1": "00001234.567",
        "1.8.2": "00001234.567",
        # ... all OBIS codes
    }

@pytest.fixture
def mock_system_response():
    """Mock system API response."""
    return {
        "deviceId": "test-device-123",
        "firmwareVersion": "1.0.0",
        "temperature": 25.5,
        # ... all system data
    }
```

### Test Coverage Areas
- [ ] P1 data parsing and sensor creation
- [ ] System data parsing and sensor creation
- [ ] Net power calculation
- [ ] Device information handling
- [ ] Error states and recovery
- [ ] Configuration validation
- [ ] Update coordination
- [ ] Entity registry integration

## 📚 References
- [Home Assistant Testing](https://developers.home-assistant.io/docs/development_testing)
- [pytest Documentation](https://docs.pytest.org/)
- [Home Assistant Test Examples](https://github.com/home-assistant/core/tree/dev/tests/components)

## 🧪 Testing Requirements
- [ ] 80%+ code coverage
- [ ] All test cases pass
- [ ] Mock external dependencies
- [ ] Test error conditions
- [ ] Test edge cases
- [ ] Performance tests for large datasets

## 💰 Grant Opportunity
This task is eligible for grants through the [Sourceful Energy Spark Initiative](https://sourceful.energy/grants).

## 🚀 Getting Started
1. Comment below to claim this issue
2. Fork the repository
3. Create feature branch: `git checkout -b feature/test-coverage`
4. Set up test structure and fixtures
5. Implement comprehensive tests
6. Verify 80%+ coverage
7. Submit PR with test documentation

## ✅ Definition of Done
- [ ] Test coverage ≥ 80%
- [ ] All sensors tested
- [ ] Error scenarios covered
- [ ] Mock fixtures created
- [ ] Tests run in CI/CD
- [ ] Test documentation added
- [ ] Performance benchmarks established 
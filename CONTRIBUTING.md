# Contributing to P1 Reader Home Assistant Custom Component

Thank you for your interest in contributing to the P1 Reader Home Assistant custom component! This document provides guidelines for contributing to the project.

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Home Assistant development environment
- Access to a Sourceful Energy Zap P1 Reader device for testing

### Development Setup

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/srcfl/spark-zap-home-assistant.git
       cd spark-zap-home-assistant
   ```

3. **Set up Home Assistant development environment**:
   ```bash
   # Create a virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install Home Assistant in development mode
   pip install homeassistant
   ```

4. **Install the custom component** in your development environment:
   ```bash
   # Link the custom component to your Home Assistant config
   ln -s $(pwd)/custom_components/p1_reader ~/.homeassistant/custom_components/p1_reader
   ```

## Development Guidelines

### Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) Python style guidelines
- Use type hints for all function parameters and return values
- Use meaningful variable and function names
- Add docstrings to all classes and functions
- Keep functions small and focused on a single responsibility

### Code Quality Tools

We recommend using these tools for code quality:

```bash
# Install development dependencies
pip install black flake8 pylint mypy

# Format code
black custom_components/

# Check for linting issues
flake8 custom_components/
pylint custom_components/

# Type checking
mypy custom_components/
```

### Testing

- Test your changes with a real P1 Reader device
- Check that all sensors are created correctly
- Verify that sensor values update properly
- Test error handling (network issues, API errors)
- Ensure no regressions in existing functionality

### Commit Messages

Use clear, descriptive commit messages:

```
feat: add support for additional OBIS codes
fix: handle connection timeout gracefully
docs: update README with new configuration options
refactor: improve error handling in data coordinator
```

## Making Changes

### Before You Start

1. **Check existing issues** to see if your bug/feature is already being worked on
2. **Create an issue** to discuss your proposed changes
3. **Create a feature branch** from main:
   ```bash
   git checkout -b feature/your-feature-name
   ```

### Making Your Changes

1. **Write code** following the guidelines above
2. **Test thoroughly** with a real device
3. **Update documentation** if needed
4. **Update CHANGELOG** if applicable
5. **Commit your changes** with clear messages

### Submitting Changes

1. **Push your branch** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a Pull Request** on GitHub:
   - Use a clear title and description
   - Reference any related issues
   - Include screenshots if applicable
   - Describe what you tested

## Types of Contributions

### Bug Fixes

- Fix incorrect sensor values
- Handle API errors gracefully
- Improve error messages
- Fix configuration issues

### New Features

- Add support for new OBIS codes
- Implement additional calculated sensors
- Add configuration options
- Improve device information

### Documentation

- Improve README
- Add examples
- Update configuration documentation
- Add troubleshooting guides

### Code Quality

- Refactor existing code
- Add type hints
- Improve error handling
- Add unit tests

## Testing Your Changes

### Manual Testing

1. **Install your changes** in a development Home Assistant instance
2. **Configure the component** with your P1 Reader
3. **Verify all sensors** are created and updating
4. **Test error scenarios**:
   - Network disconnection
   - Invalid API responses
   - Device unreachable
5. **Check logs** for any errors or warnings

### Configuration Testing

Test with different configurations:

```yaml
# Test minimal configuration
sensor:
  - platform: p1_reader
    host: zap.local

# Test full configuration
sensor:
  - platform: p1_reader
    host: 192.168.1.100
    endpoint: /api/data/p1/obis
    name: Custom P1
    scan_interval: 15
```

## Release Process

Maintainers will handle releases. Version numbers follow [Semantic Versioning](https://semver.org/):

- **Major**: Breaking changes
- **Minor**: New features, backward compatible
- **Patch**: Bug fixes, backward compatible

## Getting Help

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions and community support
- **Home Assistant Community**: For general Home Assistant help

## Code of Conduct

This project follows the [Home Assistant Code of Conduct](https://github.com/home-assistant/core/blob/dev/CODE_OF_CONDUCT.md). Please be respectful and constructive in all interactions.

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License. 
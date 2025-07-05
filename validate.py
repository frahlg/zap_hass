#!/usr/bin/env python3
"""
Validation script for Sourceful Energy Zap Home Assistant Custom Component
This script checks if the component is properly structured and configured.
"""

import json
import os
import sys
import importlib.util
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a file exists and print status."""
    if os.path.exists(file_path):
        print(f"✓ {description}: {file_path}")
        return True
    else:
        print(f"✗ {description}: {file_path} (missing)")
        return False

def validate_json_file(file_path, description):
    """Validate that a JSON file is properly formatted."""
    try:
        with open(file_path, 'r') as f:
            json.load(f)
        print(f"✓ {description}: Valid JSON")
        return True
    except json.JSONDecodeError as e:
        print(f"✗ {description}: Invalid JSON - {e}")
        return False
    except FileNotFoundError:
        print(f"✗ {description}: File not found")
        return False

def validate_python_imports(file_path, description):
    """Validate that a Python file can be imported."""
    try:
        spec = importlib.util.spec_from_file_location("module", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        print(f"✓ {description}: Imports successfully")
        return True
    except Exception as e:
        print(f"✗ {description}: Import error - {e}")
        return False

def validate_manifest_content(manifest_path):
    """Validate manifest.json content."""
    try:
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        required_fields = ['domain', 'name', 'version', 'documentation', 'codeowners']
        missing_fields = []
        
        for field in required_fields:
            if field not in manifest:
                missing_fields.append(field)
        
        if missing_fields:
            print(f"✗ Manifest validation: Missing fields: {missing_fields}")
            return False
        
        if manifest['domain'] != 'sourceful_zap':
            print(f"✗ Manifest validation: Domain should be 'sourceful_zap', got '{manifest['domain']}'")
            return False
        
        print("✓ Manifest validation: All required fields present")
        return True
    except Exception as e:
        print(f"✗ Manifest validation: Error - {e}")
        return False

def main():
    """Main validation function."""
    print("Sourceful Energy Zap Home Assistant Custom Component Validator")
    print("=" * 60)
    
    all_checks_passed = True
    
    # Check directory structure
    print("\n1. Checking directory structure...")
    base_dir = Path("custom_components/sourceful_zap")
    if not base_dir.exists():
        print(f"✗ Component directory: {base_dir} (missing)")
        print("ERROR: Component directory not found. Please run this script from the repository root.")
        return False
    
    print(f"✓ Component directory: {base_dir}")
    
    # Check required files
    print("\n2. Checking required files...")
    required_files = [
        (base_dir / "manifest.json", "Manifest file"),
        (base_dir / "__init__.py", "Init file"),
        (base_dir / "sensor.py", "Sensor file"),
        ("README.md", "README file"),
        ("LICENSE", "License file"),
        ("hacs.json", "HACS configuration"),
    ]
    
    for file_path, description in required_files:
        if not check_file_exists(file_path, description):
            all_checks_passed = False
    
    # Validate JSON files
    print("\n3. Validating JSON files...")
    json_files = [
        (base_dir / "manifest.json", "Manifest JSON"),
        ("hacs.json", "HACS JSON"),
    ]
    
    for file_path, description in json_files:
        if not validate_json_file(file_path, description):
            all_checks_passed = False
    
    # Validate manifest content
    print("\n4. Validating manifest content...")
    if not validate_manifest_content(base_dir / "manifest.json"):
        all_checks_passed = False
    
    # Check Python imports
    print("\n5. Validating Python imports...")
    python_files = [
        (base_dir / "__init__.py", "Init module"),
        (base_dir / "sensor.py", "Sensor module"),
    ]
    
    for file_path, description in python_files:
        if os.path.exists(file_path):
            if not validate_python_imports(file_path, description):
                all_checks_passed = False
    
    # Check branding files
    print("\n6. Checking branding files...")
    if not check_file_exists("icon.png", "Integration icon"):
        all_checks_passed = False
    
    # Check optional files
    print("\n7. Checking optional files...")
    optional_files = [
        ("CONTRIBUTING.md", "Contributing guidelines"),
        ("CHANGELOG.md", "Changelog"),
        ("install.sh", "Installation script"),
        ("examples/configuration.yaml", "Configuration example"),
    ]
    
    for file_path, description in optional_files:
        check_file_exists(file_path, description)
    
    # Summary
    print("\n" + "=" * 60)
    if all_checks_passed:
        print("✓ All validation checks passed!")
        print("Your Sourceful Energy Zap component is ready for use.")
        return True
    else:
        print("✗ Some validation checks failed.")
        print("Please fix the issues above before using the component.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
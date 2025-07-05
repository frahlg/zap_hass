#!/bin/bash

# Local validation script to check code formatting before pushing
# This uses Docker to match the GitHub Actions environment exactly

echo "🔍 Running local validation using Docker..."

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not available. Please install Docker to run local validation."
    exit 1
fi

# Run Black formatting check
echo "📝 Checking Black formatting..."
docker run --rm -v $(pwd):/app -w /app python:3.10-slim bash -c "pip install black && python -m black --check --diff custom_components/"

if [ $? -eq 0 ]; then
    echo "✅ Black formatting check passed!"
else
    echo "❌ Black formatting check failed. Run the following to fix:"
    echo "   docker run --rm -v \$(pwd):/app -w /app python:3.10-slim bash -c \"pip install black && python -m black custom_components/\""
    exit 1
fi

# Run basic Python syntax check
echo "🐍 Checking Python syntax..."
docker run --rm -v $(pwd):/app -w /app python:3.10-slim bash -c "python -m py_compile custom_components/sourceful_zap/__init__.py custom_components/sourceful_zap/sensor.py"

if [ $? -eq 0 ]; then
    echo "✅ Python syntax check passed!"
else
    echo "❌ Python syntax check failed."
    exit 1
fi

# Check JSON files
echo "📄 Checking JSON files..."
docker run --rm -v $(pwd):/app -w /app python:3.10-slim bash -c "python -m json.tool custom_components/sourceful_zap/manifest.json >/dev/null && python -m json.tool hacs.json >/dev/null"

if [ $? -eq 0 ]; then
    echo "✅ JSON files are valid!"
else
    echo "❌ JSON file validation failed."
    exit 1
fi

# Check icon file
echo "🎨 Checking icon file..."
if [ -f "icon.png" ]; then
    echo "✅ Icon file exists!"
else
    echo "❌ Icon file (icon.png) is missing."
    exit 1
fi

echo "🎉 All local validation checks passed! Safe to push to GitHub." 
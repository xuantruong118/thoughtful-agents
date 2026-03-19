#!/bin/bash

# Test script for Thoughtful Agents Web Demo
# This script validates the setup and provides instructions for testing

echo "=========================================="
echo "Thoughtful Agents Web Demo - Test Script"
echo "=========================================="
echo ""

# Check Python version
echo "1. Checking Python version..."
python_version=$(python --version 2>&1)
echo "   $python_version"

if python -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo "   ✓ Python version is compatible (3.8+)"
else
    echo "   ✗ Python version must be 3.8 or higher"
    exit 1
fi
echo ""

# Check if in correct directory
echo "2. Checking directory structure..."
if [ ! -d "web_demo" ]; then
    echo "   ✗ web_demo directory not found"
    echo "   Please run this script from the repository root"
    exit 1
fi
echo "   ✓ Directory structure is correct"
echo ""

# Check required files
echo "3. Checking required files..."
required_files=(
    "web_demo/app.py"
    "web_demo/templates/index.html"
    "web_demo/static/css/style.css"
    "web_demo/static/js/app.js"
    "examples/vehicle_assistant_scenario2.py"
    "examples/vehicle_assistant_extended.py"
    "requirements.txt"
)

all_files_present=true
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✓ $file"
    else
        echo "   ✗ $file (missing)"
        all_files_present=false
    fi
done

if [ "$all_files_present" = false ]; then
    echo ""
    echo "   Some required files are missing!"
    exit 1
fi
echo ""

# Check Python dependencies
echo "4. Checking Python dependencies..."
dependencies=("numpy" "openai" "spacy" "flask")

missing_deps=()
for dep in "${dependencies[@]}"; do
    if python -c "import $dep" 2>/dev/null; then
        echo "   ✓ $dep is installed"
    else
        echo "   ✗ $dep is not installed"
        missing_deps+=("$dep")
    fi
done

if [ ${#missing_deps[@]} -gt 0 ]; then
    echo ""
    echo "   Missing dependencies detected!"
    echo "   Install them with: pip install -r requirements.txt"
    echo ""
fi
echo ""

# Check OpenAI API key
echo "5. Checking OpenAI API key..."
if [ -z "$OPENAI_API_KEY" ]; then
    echo "   ✗ OPENAI_API_KEY environment variable is not set"
    echo "   Please set it with: export OPENAI_API_KEY='your-api-key'"
    echo ""
else
    echo "   ✓ OPENAI_API_KEY is set"
    echo ""
fi

# Syntax check
echo "6. Checking Python syntax..."
if python -m py_compile web_demo/app.py 2>/dev/null; then
    echo "   ✓ web_demo/app.py syntax is valid"
else
    echo "   ✗ web_demo/app.py has syntax errors"
fi

if python -m py_compile examples/vehicle_assistant_extended.py 2>/dev/null; then
    echo "   ✓ examples/vehicle_assistant_extended.py syntax is valid"
else
    echo "   ✗ examples/vehicle_assistant_extended.py has syntax errors"
fi
echo ""

# Summary
echo "=========================================="
echo "Test Summary"
echo "=========================================="
echo ""

if [ "$all_files_present" = true ] && [ ${#missing_deps[@]} -eq 0 ] && [ -n "$OPENAI_API_KEY" ]; then
    echo "✓ All checks passed! Ready to run the demo."
    echo ""
    echo "To start the web demo:"
    echo "  cd web_demo"
    echo "  python app.py"
    echo ""
    echo "Then open http://localhost:5000 in your browser"
    echo ""
else
    echo "⚠ Some checks failed. Please address the issues above."
    echo ""
    if [ ${#missing_deps[@]} -gt 0 ]; then
        echo "Install missing dependencies:"
        echo "  pip install -r requirements.txt"
        echo ""
    fi
    if [ -z "$OPENAI_API_KEY" ]; then
        echo "Set OpenAI API key:"
        echo "  export OPENAI_API_KEY='your-api-key-here'"
        echo ""
    fi
fi

echo "=========================================="
echo "Additional Test Options"
echo "=========================================="
echo ""
echo "Test the extended scenario directly (CLI):"
echo "  python examples/vehicle_assistant_extended.py"
echo ""
echo "Test the basic scenario (CLI):"
echo "  python examples/vehicle_assistant_scenario2.py"
echo ""

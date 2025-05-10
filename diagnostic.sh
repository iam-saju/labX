#!/bin/bash

# Print environment information
echo "=================== ENVIRONMENT INFO ==================="
echo "Current user: $(whoami)"
echo "Current directory: $(pwd)"
echo "Directory contents: $(ls -la)"
echo "HOME: $HOME"
echo "PATH: $PATH"
echo "Python version: $(python --version)"
echo "Django version: $(python -c 'import django; print(django.__version__)')"

# Check if we can access /app
echo "=================== APP DIRECTORY CHECK ==================="
if [ -d "/app" ]; then
    echo "/app directory exists"
    echo "/app contents: $(ls -la /app)"
    
    # Try to create staticfiles in /app
    echo "Attempting to create /app/staticfiles..."
    mkdir -p /app/staticfiles 2>&1
    echo "Result of mkdir: $?"
    
    # Check if directory was created
    if [ -d "/app/staticfiles" ]; then
        echo "/app/staticfiles created successfully"
        echo "Contents: $(ls -la /app/staticfiles)"
    else
        echo "Failed to create /app/staticfiles"
    fi
else
    echo "/app directory does not exist"
fi

# Check the BASE_DIR from Django
echo "=================== DJANGO BASE_DIR CHECK ==================="
DJANGO_BASE_DIR=$(python -c 'from pathlib import Path; import os, django; django_path = os.path.dirname(django.__file__); print(Path(django_path).resolve().parent.parent)')
echo "Django BASE_DIR equivalent: $DJANGO_BASE_DIR"

# Try alternative locations for staticfiles
echo "=================== ALTERNATIVE LOCATIONS ==================="
echo "Creating staticfiles in current directory..."
mkdir -p staticfiles
echo "Result: $?"

echo "Creating staticfiles in parent directory..."
mkdir -p ../staticfiles
echo "Result: $?"

# Check Django settings
echo "=================== DJANGO SETTINGS ==================="
echo "Checking Django settings for STATIC_ROOT..."
python -c "
import os
from pathlib import Path
# Simulate Django settings
BASE_DIR = Path(__file__).resolve().parent
STATIC_ROOT = os.environ.get('STATIC_ROOT', os.path.join(BASE_DIR, 'staticfiles'))
print(f'BASE_DIR: {BASE_DIR}')
print(f'STATIC_ROOT: {STATIC_ROOT}')
print(f'STATIC_ROOT exists: {os.path.exists(STATIC_ROOT)}')
"

# Print filesystem information
echo "=================== FILESYSTEM INFO ==================="
echo "Root directory contents: $(ls -la /)"
echo "Disk usage: $(df -h)"

# Attempt to run collectstatic in verbose mode
echo "=================== COLLECTSTATIC TEST ==================="
python -c "
import django
from django.core.management import call_command
django.setup()
try:
    call_command('collectstatic', interactive=False, verbosity=2)
    print('Collectstatic completed successfully')
except Exception as e:
    print(f'Collectstatic failed: {e}')
"

echo "=================== DIAGNOSTICS COMPLETE ==================="
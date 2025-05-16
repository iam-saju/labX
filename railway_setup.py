#!/usr/bin/env python
import os
import sys
import tempfile
import subprocess
from pathlib import Path

# Find the Django project root
BASE_DIR = Path(__file__).resolve().parent

print("="*50)
print("RAILWAY SETUP DIAGNOSTICS")
print("="*50)
print(f"Current directory: {os.getcwd()}")
print(f"Directory contents: {os.listdir('.')}")

# Define the target static files directory
staticfiles_dir = "/app/staticfiles"
print(f"Exists /app: {os.path.exists('/app')}")
print(f"Exists {staticfiles_dir}: {os.path.exists(staticfiles_dir)}")


# Try different approaches to create the staticfiles directory
print("\nTrying to create staticfiles directory...")
approaches = [
    ["mkdir", "-p", staticfiles_dir],
    ["python", "-c", f"import os; os.makedirs('{staticfiles_dir}', exist_ok=True)"],
    ["python", "-c", f"import pathlib; pathlib.Path('{staticfiles_dir}').mkdir(parents=True, exist_ok=True)"]
]

for cmd in approaches:
    try:
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(f"  Exit code: {result.returncode}")
        if result.stdout:
            print(f"  Output: {result.stdout}")
        if result.stderr:
            print(f"  Error: {result.stderr}")
    except Exception as e:
        print(f"  Exception: {e}")

print("\nStarting normal Django process...")
print("="*50)

# No need to execute any command, just exit successfully
# Railway will continue with the next commands in the Procfile
sys.exit(0)
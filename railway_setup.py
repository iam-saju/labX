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

# **REMOVE THE PATCHING SECTION HERE**
# The following block of code that modifies settings.py should be removed
# or commented out:

# print("\nPatching Django settings...")
# settings_file = os.path.join(BASE_DIR, "backend", "settings.py")
#
# if os.path.exists(settings_file):
#     with open(settings_file, 'r') as f:
#         settings_content = f.read()
#
#     # Check if we've already patched the file
#     if "# RAILWAY STATIC FILES PATCH" not in settings_content:
#         patch = """
# # RAILWAY STATIC FILES PATCH
# import tempfile
# STATIC_URL = '/static/'
# STATIC_ROOT = tempfile.gettempdir()  # Use system temp directory
# print(f"Using temp directory for static files: {STATIC_ROOT}")
# # End of patch
# """
#         with open(settings_file, 'a') as f:
#             f.write(patch)
#         print("Settings patched to use temp directory for static files")
#     else:
#         print("Settings already patched")
# else:
#     print(f"Settings file not found at {settings_file}")

print("\nStarting normal Django process...")
print("="*50)

# Continue with normal startup (collectstatic and gunicorn)
# The execvp call executes the rest of the command from the Procfile
if len(sys.argv) > 1:
    try:
         # Use os.execvp to replace the current process with the new one
         os.execvp(sys.argv[1], sys.argv[1:])
    except FileNotFoundError:
         print(f"Error: Command not found: {sys.argv[1]}")
         sys.exit(1)
    except Exception as e:
        print(f"Error executing command: {e}")
        sys.exit(1)
else:
    print("Error: No command provided to execute after setup.")
    sys.exit(1)
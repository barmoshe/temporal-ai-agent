#!/usr/bin/env python3
"""
Run Tool Tests

This script runs the tool tests with the test environment.
It automatically uses the project's virtual environment if it exists.
"""
import os
import sys
import unittest
import argparse
import subprocess
from pathlib import Path

# Check if we're in the virtual environment
in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

# If not in venv and venv exists, re-execute this script in the venv
if not in_venv:
    venv_python = Path(__file__).resolve().parent.parent / 'venv' / 'bin' / 'python'
    if venv_python.exists():
        print(f"Re-running with virtual environment: {venv_python}")
        os.execl(str(venv_python), str(venv_python), *sys.argv)

# Set the .env.test file as the environment file
os.environ["DOTENV_FILE"] = ".env.test"

# Parse arguments
parser = argparse.ArgumentParser(description="Run tool tests")
parser.add_argument("test_path", nargs="?", default="test_tools.py", help="Test file or directory to run")
parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
args = parser.parse_args()

# Add mock_modules to path if it exists
mock_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "mock_modules")
if os.path.exists(mock_dir):
    sys.path.insert(0, mock_dir)

# Print information about the environment
print(f"Using Python: {sys.executable}")
print(f"In virtual environment: {in_venv}")

# Run the tests
if os.path.exists(args.test_path):
    if os.path.isdir(args.test_path):
        # Discover tests in the directory
        test_loader = unittest.TestLoader()
        test_suite = test_loader.discover(args.test_path)
    else:
        # Load tests from the specific file
        test_loader = unittest.TestLoader()
        test_suite = test_loader.discover(os.path.dirname(args.test_path), pattern=os.path.basename(args.test_path))
    
    runner = unittest.TextTestRunner(verbosity=2 if args.verbose else 1)
    runner.run(test_suite)
else:
    print(f"Error: Test path '{args.test_path}' does not exist.")
    sys.exit(1)

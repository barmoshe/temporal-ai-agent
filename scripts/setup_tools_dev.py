#!/usr/bin/env python3
"""
Setup Tools Development Environment

This script sets up the development environment for working with tools.
It ensures that all necessary dependencies are installed and the environment is properly configured.
It automatically uses the project's virtual environment if it exists.
"""
import os
import sys
import subprocess
import argparse
from pathlib import Path

# Check if we're in the virtual environment
in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

# If not in venv and venv exists, re-execute this script in the venv
if not in_venv:
    venv_python = Path(__file__).resolve().parent.parent / 'venv' / 'bin' / 'python'
    if venv_python.exists():
        print(f"Re-running with virtual environment: {venv_python}")
        os.execl(str(venv_python), str(venv_python), *sys.argv)

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import dotenv
        print("✅ python-dotenv is installed")
    except ImportError:
        print("❌ python-dotenv is not installed")
        install_package("python-dotenv")
    
    # Mock the missing dependencies for testing
    required_packages = [
        "stripe",  # Used by create_invoice.py
    ]
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is not installed")
            if not args.mock:
                install_package(package)
            else:
                create_mock_module(package)


def install_package(package):
    """Install a Python package using pip."""
    print(f"Installing {package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    print(f"✅ {package} has been installed")


def create_mock_module(package):
    """Create a mock module for testing purposes."""
    mock_dir = Path("mock_modules")
    mock_dir.mkdir(exist_ok=True)
    
    # Add the mock_modules directory to Python path
    sys.path.insert(0, str(mock_dir.absolute()))
    
    # Create an empty module file
    module_file = mock_dir / f"{package}.py"
    module_file.write_text("# Mock module for testing\n")
    
    # Create an __init__.py file if it doesn't exist
    init_file = mock_dir / "__init__.py"
    if not init_file.exists():
        init_file.write_text("# Mock modules package\n")
    
    print(f"✅ Created mock module for {package}")


def setup_test_environment():
    """Set up the test environment for tools."""
    # Create a .env.test file if it doesn't exist
    env_test_file = Path(".env.test")
    if not env_test_file.exists():
        env_test_file.write_text("""# Test environment variables
RAPIDAPI_KEY=test_key
RAPIDAPI_HOST=test_host
LLM_PROVIDER=openai
OPENAI_API_KEY=test_openai_key
""")
        print("✅ Created .env.test file")
    
    # Create a tools/test directory if it doesn't exist
    test_dir = Path("tools/test")
    test_dir.mkdir(exist_ok=True)
    
    # Create an __init__.py file in the test directory
    init_file = test_dir / "__init__.py"
    if not init_file.exists():
        init_file.write_text("# Test package\n")
        print("✅ Created tools/test/__init__.py")


def create_env_test_runner():
    """Create a script to run tests with the test environment."""
    script_path = Path("scripts/run_tool_tests.py")
    script_content = """#!/usr/bin/env python3
\"\"\"
Run Tool Tests

This script runs the tool tests with the test environment.
It automatically uses the project's virtual environment if it exists.
\"\"\"
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
"""
    script_path.write_text(script_content)
    script_path.chmod(0o755)  # Make executable
    print("✅ Created test runner script at scripts/run_tool_tests.py")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Setup tools development environment")
    parser.add_argument("--mock", action="store_true", help="Create mock modules instead of installing packages")
    args = parser.parse_args()
    
    # Print information about the environment
    print(f"Using Python: {sys.executable}")
    print(f"In virtual environment: {in_venv}")
    
    print("Setting up tools development environment...")
    check_dependencies()
    setup_test_environment()
    create_env_test_runner()
    print("\n🎉 Tools development environment setup complete!")
    print("\nTo run tests, use: python scripts/run_tool_tests.py")
    if args.mock:
        print("\nNote: Mock modules have been created for missing dependencies.")
        print("These mocks may not work for all tests, but they should allow basic testing.") 
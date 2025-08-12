#!/usr/bin/env python3
"""
Test runner script for the MCP Server project.
"""

import sys
import subprocess
import os


def install_dependencies():
    """Install test dependencies."""
    print("Installing test dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    return True


def run_tests():
    """Run the test suite."""
    print("Running tests...")
    try:
        # Run tests with coverage
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/", 
            "-v", 
            "--cov=src",
            "--cov-report=term-missing",
            "--cov-report=html:htmlcov"
        ])
        
        if result.returncode == 0:
            print("✅ All tests passed!")
        else:
            print("❌ Some tests failed!")
        
        return result.returncode == 0
        
    except FileNotFoundError:
        print("❌ pytest not found. Please install it with: pip install pytest pytest-cov")
        return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Test execution failed: {e}")
        return False


def run_unit_tests():
    """Run only unit tests."""
    print("Running unit tests...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/test_example_tools.py", 
            "-v", 
            "-m", "unit"
        ])
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Unit test execution failed: {e}")
        return False


def run_integration_tests():
    """Run only integration tests."""
    print("Running integration tests...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/test_main.py", 
            "tests/test_integration.py", 
            "-v", 
            "-m", "integration"
        ])
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Integration test execution failed: {e}")
        return False


def main():
    """Main function."""
    print("🧪 MCP Server Test Runner")
    print("=" * 40)
    
    # Check if we should install dependencies
    if len(sys.argv) > 1 and sys.argv[1] == "--install":
        if not install_dependencies():
            sys.exit(1)
    
    # Check command line arguments
    if len(sys.argv) > 1:
        test_type = sys.argv[1]
        if test_type == "unit":
            success = run_unit_tests()
        elif test_type == "integration":
            success = run_integration_tests()
        elif test_type == "all":
            success = run_tests()
        else:
            print(f"Unknown test type: {test_type}")
            print("Available options: unit, integration, all")
            sys.exit(1)
    else:
        # Default: run all tests
        success = run_tests()
    
    if success:
        print("\n🎉 Test execution completed successfully!")
        sys.exit(0)
    else:
        print("\n💥 Test execution failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()

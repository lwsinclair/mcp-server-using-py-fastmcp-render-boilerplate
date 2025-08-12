"""
Pytest configuration and common fixtures.
"""

import pytest
import logging
import tempfile
import os
from unittest.mock import patch


@pytest.fixture(scope="session")
def temp_log_file():
    """Create a temporary log file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as f:
        temp_log_path = f.name
    
    yield temp_log_path
    
    # Cleanup
    if os.path.exists(temp_log_path):
        os.unlink(temp_log_path)


@pytest.fixture(autouse=True)
def reset_logging():
    """Reset logging configuration before each test."""
    # Clear all handlers from root logger
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Reset logging level
    root_logger.setLevel(logging.WARNING)
    
    yield
    
    # Cleanup after test
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)


@pytest.fixture
def sample_echo_data():
    """Sample data for echo tool tests."""
    return {
        "simple": "Hello, World!",
        "empty": "",
        "special_chars": "!@#$%^&*()_+-=[]{}|;':\",./<>?",
        "unicode": "Hello 世界 🌍",
        "numbers": "12345",
        "long_text": "This is a very long message that contains many characters and should be handled properly by the echo tool without any issues."
    }


@pytest.fixture
def sample_calculator_data():
    """Sample data for calculator tool tests."""
    return {
        "add": {"a": 5, "b": 3, "expected": 8},
        "subtract": {"a": 10, "b": 4, "expected": 6},
        "multiply": {"a": 6, "b": 7, "expected": 42},
        "divide": {"a": 15, "b": 3, "expected": 5.0},
        "divide_float": {"a": 10, "b": 3, "expected": 3.3333333333333335},
        "negative": {"a": -5, "b": 3, "expected": -2},
        "zero": {"a": 0, "b": 5, "expected": 5},
        "large": {"a": 999999999, "b": 1, "expected": 1000000000}
    }


@pytest.fixture
def mock_environment():
    """Mock environment variables for testing."""
    env_vars = {
        'MCP_SERVER_NAME': 'test-mcp-server',
        'HOST': '127.0.0.1',
        'PORT': '8080',
        'DEBUG': 'true'
    }
    
    with patch.dict(os.environ, env_vars):
        yield env_vars


@pytest.fixture
def mock_fastmcp():
    """Mock FastMCP instance for testing."""
    with patch('main.FastMCP') as mock:
        mock_instance = mock.return_value
        yield mock_instance


# Pytest configuration
def pytest_configure(config):
    """Configure pytest."""
    # Add custom markers
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection."""
    for item in items:
        # Mark tests based on their location
        if "test_example_tools" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "test_main" in str(item.fspath):
            item.add_marker(pytest.mark.integration)

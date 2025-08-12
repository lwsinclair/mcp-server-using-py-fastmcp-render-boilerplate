# Testing Guide for MCP Server

This document provides comprehensive information about the testing setup for the MCP Server project.

Simple test run

```bash
python -m pytest tests/ -v
```

## Overview

The project includes a comprehensive test suite built with pytest that covers:

- **Unit Tests**: Individual function testing
- **Integration Tests**: End-to-end workflow testing
- **Performance Tests**: Stress and load testing
- **Error Handling Tests**: Exception and edge case testing

## Test Structure

```
tests/
├── __init__.py              # Tests package
├── conftest.py             # Pytest configuration and fixtures
├── test_example_tools.py   # Unit tests for tools
├── test_main.py            # Tests for main application
└── test_integration.py     # Integration tests
```

## Prerequisites

Before running tests, ensure you have the required dependencies:

```bash
# Install test dependencies
pip install -r requirements.txt
```

Or use the test runner:

```bash
python run_tests.py --install
```

## Running Tests

### Using the Test Runner (Recommended)

The project includes a convenient test runner script:

```bash
# Run all tests with coverage
python run_tests.py

# Run only unit tests
python run_tests.py unit

# Run only integration tests
python run_tests.py integration

# Run all tests
python run_tests.py all
```

### Using pytest Directly

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src --cov-report=html

# Run specific test file
pytest tests/test_example_tools.py -v

# Run tests by marker
pytest tests/ -v -m unit
pytest tests/ -v -m integration
pytest tests/ -v -m "not slow"
```

## Test Categories

### Unit Tests (`test_example_tools.py`)

Tests individual functions in isolation:

- **Echo Tool Tests**: Message echoing functionality
- **Calculator Tool Tests**: Arithmetic operations
- **Edge Cases**: Boundary conditions and error handling

### Integration Tests (`test_integration.py`)

Tests how components work together:

- **Tool Workflow Tests**: Multiple tools working in sequence
- **MCP Server Integration**: Tool registration and server setup
- **Performance Tests**: Load and stress testing
- **Error Recovery**: System resilience testing

### Main Application Tests (`test_main.py`)

Tests the main application logic:

- **Configuration Tests**: Environment variable handling
- **Logging Tests**: Log setup and configuration
- **Server Setup Tests**: MCP server initialization

## Test Markers

The test suite uses pytest markers for organization:

- `@pytest.mark.unit`: Unit tests
- `@pytest.mark.integration`: Integration tests
- `@pytest.mark.slow`: Tests that take longer to run

## Coverage Reports

The test suite generates coverage reports:

- **Terminal Output**: Shows missing lines
- **HTML Report**: Detailed coverage in `htmlcov/` directory
- **XML Report**: For CI/CD integration

## Test Fixtures

Common test fixtures are defined in `conftest.py`:

- `sample_echo_data`: Test data for echo tool
- `sample_calculator_data`: Test data for calculator tool
- `mock_environment`: Mock environment variables
- `mock_fastmcp`: Mock FastMCP instance
- `reset_logging`: Automatic logging cleanup

## Writing New Tests

### Adding Unit Tests

1. Create test functions in the appropriate test file
2. Use descriptive test names starting with `test_`
3. Include docstrings explaining what is being tested
4. Use appropriate assertions and error checking

Example:
```python
def test_new_feature():
    """Test the new feature functionality."""
    result = new_feature("input")
    assert result["status"] == "success"
    assert "output" in result
```

### Adding Integration Tests

1. Test workflows involving multiple components
2. Use the `@pytest.mark.integration` marker
3. Test error scenarios and recovery
4. Include performance considerations

### Adding Performance Tests

1. Use the `@pytest.mark.slow` marker for long-running tests
2. Test with realistic data volumes
3. Include timing assertions
4. Test memory usage and cleanup

## Continuous Integration

The test suite is designed to work with CI/CD systems:

- Tests run in parallel where possible
- Coverage reports are generated
- Exit codes indicate success/failure
- XML reports for CI integration

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure you're running from the project root
2. **Missing Dependencies**: Run `pip install -r requirements.txt`
3. **Test Failures**: Check the test output for specific error messages
4. **Coverage Issues**: Ensure all code paths are tested

### Debugging Tests

```bash
# Run tests with more verbose output
pytest tests/ -v -s

# Run a specific test with debugging
pytest tests/test_example_tools.py::TestEchoTool::test_echo_tool_basic -v -s

# Run tests with print statements visible
pytest tests/ -v -s --capture=no
```

## Best Practices

1. **Test Naming**: Use descriptive test names that explain the scenario
2. **Test Isolation**: Each test should be independent
3. **Cleanup**: Use fixtures for setup and teardown
4. **Assertions**: Use specific assertions with meaningful messages
5. **Documentation**: Include docstrings for complex tests
6. **Coverage**: Aim for high test coverage but focus on critical paths

## Performance Considerations

- Unit tests should run quickly (< 1 second each)
- Integration tests may take longer but should be reasonable
- Use `@pytest.mark.slow` for tests that take > 5 seconds
- Consider parallel execution for large test suites

## Contributing

When adding new features:

1. Write tests first (TDD approach)
2. Ensure all new code is covered by tests
3. Update this documentation if needed
4. Run the full test suite before submitting

## Support

For questions about the testing setup:

1. Check this documentation
2. Review existing test examples
3. Check pytest documentation
4. Open an issue for specific problems

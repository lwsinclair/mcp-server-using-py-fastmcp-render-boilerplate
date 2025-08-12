"""
Tests for the example tools module.
"""

import pytest
from datetime import datetime
from src.tools.example_tools import echo_tool, calculator_tool


class TestEchoTool:
    """Test cases for the echo_tool function."""
    
    def test_echo_tool_basic(self):
        """Test basic echo functionality."""
        message = "Hello, World!"
        result = echo_tool(message)
        
        assert result["echoed_message"] == message
        assert result["tool_name"] == "echo_tool"
        assert "timestamp" in result
        
        # Verify timestamp is valid ISO format
        datetime.fromisoformat(result["timestamp"])
    
    def test_echo_tool_empty_string(self):
        """Test echo with empty string."""
        result = echo_tool("")
        
        assert result["echoed_message"] == ""
        assert result["tool_name"] == "echo_tool"
        assert "timestamp" in result
    
    def test_echo_tool_special_characters(self):
        """Test echo with special characters."""
        message = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
        result = echo_tool(message)
        
        assert result["echoed_message"] == message
        assert result["tool_name"] == "echo_tool"
    
    def test_echo_tool_unicode(self):
        """Test echo with unicode characters."""
        message = "Hello 世界 🌍"
        result = echo_tool(message)
        
        assert result["echoed_message"] == message
        assert result["tool_name"] == "echo_tool"


class TestCalculatorTool:
    """Test cases for the calculator_tool function."""
    
    def test_calculator_add(self):
        """Test addition operation."""
        result = calculator_tool("add", 5, 3)
        
        assert result["operation"] == "add"
        assert result["a"] == 5
        assert result["b"] == 3
        assert result["result"] == 8
        assert "timestamp" in result
    
    def test_calculator_subtract(self):
        """Test subtraction operation."""
        result = calculator_tool("subtract", 10, 4)
        
        assert result["operation"] == "subtract"
        assert result["a"] == 10
        assert result["b"] == 4
        assert result["result"] == 6
        assert "timestamp" in result
    
    def test_calculator_multiply(self):
        """Test multiplication operation."""
        result = calculator_tool("multiply", 6, 7)
        
        assert result["operation"] == "multiply"
        assert result["a"] == 6
        assert result["b"] == 7
        assert result["result"] == 42
        assert "timestamp" in result
    
    def test_calculator_divide(self):
        """Test division operation."""
        result = calculator_tool("divide", 15, 3)
        
        assert result["operation"] == "divide"
        assert result["a"] == 15
        assert result["b"] == 3
        assert result["result"] == 5.0
        assert "timestamp" in result
    
    def test_calculator_divide_float(self):
        """Test division with float result."""
        result = calculator_tool("divide", 10, 3)
        
        assert result["operation"] == "divide"
        assert result["a"] == 10
        assert result["b"] == 3
        assert abs(result["result"] - 3.3333333333333335) < 1e-10
        assert "timestamp" in result
    
    def test_calculator_negative_numbers(self):
        """Test operations with negative numbers."""
        result = calculator_tool("add", -5, 3)
        assert result["result"] == -2
        
        result = calculator_tool("multiply", -4, -6)
        assert result["result"] == 24
    
    def test_calculator_zero_operations(self):
        """Test operations with zero."""
        result = calculator_tool("add", 0, 5)
        assert result["result"] == 5
        
        result = calculator_tool("multiply", 0, 10)
        assert result["result"] == 0
    
    def test_calculator_invalid_operation(self):
        """Test calculator with invalid operation."""
        with pytest.raises(ValueError, match="Unsupported operation"):
            calculator_tool("invalid_op", 5, 3)
    
    def test_calculator_divide_by_zero(self):
        """Test division by zero."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            calculator_tool("divide", 10, 0)
    
    def test_calculator_float_inputs(self):
        """Test calculator with float inputs."""
        result = calculator_tool("add", 3.5, 2.5)
        assert result["result"] == 6.0
        
        result = calculator_tool("multiply", 2.5, 3.0)
        assert result["result"] == 7.5


class TestCalculatorToolEdgeCases:
    """Test edge cases for calculator tool."""
    
    def test_calculator_large_numbers(self):
        """Test with large numbers."""
        result = calculator_tool("add", 999999999, 1)
        assert result["result"] == 1000000000
    
    def test_calculator_small_decimals(self):
        """Test with very small decimal numbers."""
        result = calculator_tool("multiply", 0.1, 0.1)
        assert abs(result["result"] - 0.01) < 1e-10
    
    def test_calculator_all_operations_consistency(self):
        """Test that all operations return consistent structure."""
        operations = ["add", "subtract", "multiply", "divide"]
        
        for op in operations:
            if op == "divide":
                result = calculator_tool(op, 10, 2)
            else:
                result = calculator_tool(op, 5, 3)
            
            # Check all required keys are present
            assert "operation" in result
            assert "a" in result
            assert "b" in result
            assert "result" in result
            assert "timestamp" in result
            
            # Check operation matches
            assert result["operation"] == op

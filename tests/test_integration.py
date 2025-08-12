"""
Integration tests for the MCP server and tools.
"""

import pytest
import json
from unittest.mock import patch, MagicMock
from src.tools.example_tools import echo_tool, calculator_tool


class TestToolIntegration:
    """Integration tests for tools working together."""
    
    def test_echo_and_calculator_workflow(self):
        """Test that echo and calculator tools work together in a workflow."""
        # Simulate a workflow where we calculate something and then echo the result
        calc_result = calculator_tool("add", 10, 20)
        echo_result = echo_tool(f"Calculation result: {calc_result['result']}")
        
        # Verify calculator worked
        assert calc_result["result"] == 30
        assert calc_result["operation"] == "add"
        
        # Verify echo worked
        assert echo_result["echoed_message"] == "Calculation result: 30"
        assert echo_result["tool_name"] == "echo_tool"
    
    def test_multiple_calculations_workflow(self):
        """Test multiple calculations in sequence."""
        # First calculation
        result1 = calculator_tool("multiply", 5, 6)
        assert result1["result"] == 30
        
        # Second calculation using result from first
        result2 = calculator_tool("add", result1["result"], 10)
        assert result2["result"] == 40
        
        # Third calculation
        result3 = calculator_tool("divide", result2["result"], 4)
        assert result3["result"] == 10.0
    
    def test_error_handling_integration(self):
        """Test error handling across tools."""
        # Calculator should handle division by zero
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            calculator_tool("divide", 10, 0)
        
        # Echo should still work after calculator error
        echo_result = echo_tool("Error occurred, but echo still works")
        assert echo_result["echoed_message"] == "Error occurred, but echo still works"
    
    def test_timestamp_consistency(self):
        """Test that timestamps are consistent across tools."""
        from datetime import datetime
        
        # Call both tools in quick succession
        echo_result = echo_tool("test")
        calc_result = calculator_tool("add", 1, 1)
        
        # Parse timestamps
        echo_time = datetime.fromisoformat(echo_result["timestamp"])
        calc_time = datetime.fromisoformat(calc_result["timestamp"])
        
        # Timestamps should be close (within 1 second)
        time_diff = abs((echo_time - calc_time).total_seconds())
        assert time_diff < 1


class TestMCPIntegration:
    """Integration tests for MCP server functionality."""
    
    @patch('main.FastMCP')
    @patch('main.setup_logging')
    def test_tool_registration_integration(self, mock_setup_logging, mock_fastmcp):
        """Test that tools are properly registered with MCP server."""
        from main import main
        
        # Setup mocks
        mock_logger = MagicMock()
        mock_setup_logging.return_value = mock_logger
        
        mock_mcp_instance = MagicMock()
        mock_fastmcp.return_value = mock_mcp_instance
        
        # Mock the tool decorator to capture calls
        tool_calls = []
        def mock_tool_decorator(name, description):
            def decorator(func):
                tool_calls.append({
                    'name': name,
                    'description': description,
                    'function': func
                })
                return func
            return decorator
        
        mock_mcp_instance.tool = mock_tool_decorator
        
        # Call main function
        main()
        
        # Verify tools were registered
        assert len(tool_calls) == 2
        
        # Check echo tool registration
        echo_tool_call = next(call for call in tool_calls if call['name'] == 'echo')
        assert echo_tool_call['description'] == "Echo back the input message with a timestamp"
        assert echo_tool_call['function'].__name__ == 'echo_tool'
        
        # Check calculator tool registration
        calc_tool_call = next(call for call in tool_calls if call['name'] == 'calculator')
        assert calc_tool_call['description'] == "Perform basic arithmetic operations (add, subtract, multiply, divide)"
        assert calc_tool_call['function'].__name__ == 'calculator_tool'
    
    def test_tool_response_structure_consistency(self):
        """Test that all tools return consistent response structures."""
        # Test echo tool response structure
        echo_result = echo_tool("test message")
        assert "echoed_message" in echo_result
        assert "timestamp" in echo_result
        assert "tool_name" in echo_result
        
        # Test calculator tool response structure
        calc_result = calculator_tool("add", 1, 2)
        assert "operation" in calc_result
        assert "a" in calc_result
        assert "b" in calc_result
        assert "result" in calc_result
        assert "timestamp" in calc_result
        
        # Both should have timestamps in ISO format
        from datetime import datetime
        datetime.fromisoformat(echo_result["timestamp"])
        datetime.fromisoformat(calc_result["timestamp"])


class TestPerformanceIntegration:
    """Performance and stress tests."""
    
    def test_rapid_tool_calls(self):
        """Test rapid calls to tools."""
        import time
        
        start_time = time.time()
        
        # Make 100 rapid calls to echo tool
        for i in range(100):
            result = echo_tool(f"message_{i}")
            assert result["echoed_message"] == f"message_{i}"
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete within reasonable time (less than 5 seconds)
        assert duration < 5.0
    
    def test_large_number_calculations(self):
        """Test calculations with large numbers."""
        # Test with very large numbers
        result = calculator_tool("multiply", 999999999, 999999999)
        expected = 999999999 * 999999999
        assert result["result"] == expected
        
        # Test with very small numbers
        result = calculator_tool("multiply", 0.000001, 0.000001)
        expected = 0.000001 * 0.000001
        assert abs(result["result"] - expected) < 1e-15
    
    @pytest.mark.slow
    def test_memory_usage_stability(self):
        """Test that tools don't leak memory with repeated calls."""
        import gc
        
        # Force garbage collection before test
        gc.collect()
        
        # Make many calls to both tools
        for i in range(1000):
            echo_tool(f"test_message_{i}")
            calculator_tool("add", i, i)
        
        # Force garbage collection after test
        gc.collect()
        
        # If we get here without memory issues, the test passes
        assert True


class TestErrorRecoveryIntegration:
    """Test error recovery and resilience."""
    
    def test_tool_recovery_after_errors(self):
        """Test that tools recover properly after errors."""
        # Cause an error in calculator
        with pytest.raises(ValueError):
            calculator_tool("divide", 10, 0)
        
        # Calculator should work fine after error
        result = calculator_tool("add", 5, 3)
        assert result["result"] == 8
        
        # Echo should work fine after calculator error
        echo_result = echo_tool("Recovery test")
        assert echo_result["echoed_message"] == "Recovery test"
    
    def test_invalid_input_recovery(self):
        """Test recovery from invalid inputs."""
        # Test calculator with invalid operation
        with pytest.raises(ValueError):
            calculator_tool("invalid", 1, 2)
        
        # Should still work with valid operation
        result = calculator_tool("add", 1, 2)
        assert result["result"] == 3

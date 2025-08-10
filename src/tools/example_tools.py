"""
Example MCP tools implementation.

This module contains example tools that demonstrate how to create
and register MCP tools using FastMCP.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

# Create logger for this module
logger = logging.getLogger(__name__)

# Echo tool
def echo_tool(message: str) -> Dict[str, Any]:
    """
    Echo tool that returns the input message.
    
    Args:
        message: The message to echo back
        
    Returns:
        Dictionary containing the echoed message and timestamp
    """
    logger.info(f"Echo tool called with message: {message}")
    
    try:
        result = {
            "echoed_message": message,
            "timestamp": datetime.now().isoformat(),
            "tool_name": "echo_tool"
        }
        
        logger.debug(f"Echo tool result: {result}")
        logger.info("Echo tool completed successfully")
        return result
        
    except Exception as e:
        logger.error(f"Echo tool failed: {e}")
        raise

# Calculator tool
def calculator_tool(operation: str, a: float, b: float) -> Dict[str, Any]:
    """
    Simple calculator tool that performs basic arithmetic operations.
    
    Args:
        operation: The operation to perform ('add', 'subtract', 'multiply', 'divide')
        a: First number
        b: Second number
        
    Returns:
        Dictionary containing the result and operation details
    """
    logger.info(f"Calculator tool called: {operation}({a}, {b})")
    
    try:
        operations = {
            "add": lambda x, y: x + y,
            "subtract": lambda x, y: x - y,
            "multiply": lambda x, y: x * y,
            "divide": lambda x, y: x / y if y != 0 else None
        }
        
        if operation not in operations:
            error_msg = f"Unsupported operation: {operation}. Supported operations: {list(operations.keys())}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        if operation == "divide" and b == 0:
            error_msg = "Cannot divide by zero"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        result = operations[operation](a, b)
        
        response = {
            "operation": operation,
            "a": a,
            "b": b,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.debug(f"Calculator tool result: {response}")
        logger.info(f"Calculator tool completed: {operation}({a}, {b}) = {result}")
        return response
        
    except Exception as e:
        logger.error(f"Calculator tool failed: {e}")
        raise
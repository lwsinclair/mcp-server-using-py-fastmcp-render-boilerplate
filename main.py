#!/usr/bin/env python3
"""
Main entry point for the MCP Server using FastMCP.
"""

import os
import logging
from dotenv import load_dotenv
from fastmcp import FastMCP

# Import the tools from src/tools/example_tools.py
from src.tools.example_tools import (
    echo_tool,
    calculator_tool
)

# Load environment variables
load_dotenv()

# Configure logging
def setup_logging(debug: bool = False):
    """Setup logging configuration."""
    log_level = logging.DEBUG if debug else logging.INFO
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.StreamHandler(),  # Console handler
            logging.FileHandler('mcp_server.log')  # File handler
        ]
    )
    
    # Create logger for this module
    logger = logging.getLogger(__name__)
    logger.info("Logging configured successfully")
    return logger

def main():
    # Get configuration from environment variables
    NAME = os.getenv("MCP_SERVER_NAME", "my-mcp-server")
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "10000"))
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"

    # Setup logging
    logger = setup_logging(DEBUG)
    
    logger.info(f"Starting MCP Server: {NAME}")
    logger.info(f"Server will run on {HOST}:{PORT}")
    logger.debug(f"Debug mode: {DEBUG}")

    try:
        # Create the MCP server
        logger.info("Creating FastMCP instance...")
        mcp = FastMCP(
            name=NAME
        )
        logger.info("FastMCP instance created successfully")

        # Register the tools with the MCP server
        logger.info("Registering tools...")
        
        mcp.tool(
            name="echo",
            description="Echo back the input message with a timestamp"
        )(echo_tool)
        logger.info("Echo tool registered")
        
        mcp.tool(
            name="calculator",
            description="Perform basic arithmetic operations (add, subtract, multiply, divide)"
        )(calculator_tool)
        logger.info("Calculator tool registered")
        
        logger.info("All tools registered successfully")

        # Run the MCP server
        logger.info("Starting MCP server...")
        mcp.run(
            transport="http",
            host=HOST,
            port=PORT
        )
        
    except Exception as e:
        logger.error(f"Failed to start MCP server: {e}")
        raise

if __name__ == "__main__":
    main()
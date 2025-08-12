"""
Tests for the main application module.
"""

import pytest
import os
import logging
from unittest.mock import patch, MagicMock
from main import setup_logging, main


class TestSetupLogging:
    """Test cases for the setup_logging function."""
    
    def test_setup_logging_info_level(self):
        """Test logging setup with INFO level."""
        logger = setup_logging(debug=False)
        
        assert logger.level == logging.INFO
        assert logger.name == "__main__"
    
    def test_setup_logging_debug_level(self):
        """Test logging setup with DEBUG level."""
        logger = setup_logging(debug=True)
        
        assert logger.level == logging.DEBUG
        assert logger.name == "__main__"
    
    def test_setup_logging_handlers(self):
        """Test that logging handlers are properly configured."""
        logger = setup_logging(debug=False)
        
        # Check that handlers exist
        assert len(logger.handlers) > 0
        
        # Check that root logger has handlers
        root_logger = logging.getLogger()
        assert len(root_logger.handlers) > 0


class TestMainFunction:
    """Test cases for the main function."""
    
    @patch('main.FastMCP')
    @patch('main.setup_logging')
    @patch.dict(os.environ, {
        'MCP_SERVER_NAME': 'test-server',
        'HOST': '127.0.0.1',
        'PORT': '8080',
        'DEBUG': 'true'
    })
    def test_main_with_environment_variables(self, mock_setup_logging, mock_fastmcp):
        """Test main function with environment variables."""
        # Setup mocks
        mock_logger = MagicMock()
        mock_setup_logging.return_value = mock_logger
        
        mock_mcp_instance = MagicMock()
        mock_fastmcp.return_value = mock_mcp_instance
        
        # Call main function
        main()
        
        # Verify FastMCP was created with correct name
        mock_fastmcp.assert_called_once_with(name='test-server')
        
        # Verify tools were registered
        assert mock_mcp_instance.tool.call_count == 2
        
        # Verify server was started
        mock_mcp_instance.run.assert_called_once_with(
            transport="http",
            host="127.0.0.1",
            port=8080
        )
    
    @patch('main.FastMCP')
    @patch('main.setup_logging')
    @patch.dict(os.environ, {}, clear=True)
    def test_main_with_default_values(self, mock_setup_logging, mock_fastmcp):
        """Test main function with default values."""
        # Setup mocks
        mock_logger = MagicMock()
        mock_setup_logging.return_value = mock_logger
        
        mock_mcp_instance = MagicMock()
        mock_fastmcp.return_value = mock_mcp_instance
        
        # Call main function
        main()
        
        # Verify FastMCP was created with default name
        mock_fastmcp.assert_called_once_with(name='my-mcp-server')
        
        # Verify server was started with default values
        mock_mcp_instance.run.assert_called_once_with(
            transport="http",
            host="0.0.0.0",
            port=10000
        )
    
    @patch('main.FastMCP')
    @patch('main.setup_logging')
    @patch.dict(os.environ, {
        'MCP_SERVER_NAME': 'test-server',
        'HOST': 'localhost',
        'PORT': '9000',
        'DEBUG': 'false'
    })
    def test_main_debug_false(self, mock_setup_logging, mock_fastmcp):
        """Test main function with debug set to false."""
        # Setup mocks
        mock_logger = MagicMock()
        mock_setup_logging.return_value = mock_logger
        
        mock_mcp_instance = MagicMock()
        mock_fastmcp.return_value = mock_mcp_instance
        
        # Call main function
        main()
        
        # Verify setup_logging was called with debug=False
        mock_setup_logging.assert_called_once_with(False)
    
    @patch('main.FastMCP')
    @patch('main.setup_logging')
    def test_main_fastmcp_creation_error(self, mock_setup_logging, mock_fastmcp):
        """Test main function when FastMCP creation fails."""
        # Setup mocks
        mock_logger = MagicMock()
        mock_setup_logging.return_value = mock_logger
        
        # Make FastMCP raise an exception
        mock_fastmcp.side_effect = Exception("FastMCP creation failed")
        
        # Call main function and expect it to raise the exception
        with pytest.raises(Exception, match="FastMCP creation failed"):
            main()
        
        # Verify error was logged
        mock_logger.error.assert_called_with("Failed to start MCP server: FastMCP creation failed")
    
    @patch('main.FastMCP')
    @patch('main.setup_logging')
    def test_main_server_run_error(self, mock_setup_logging, mock_fastmcp):
        """Test main function when server run fails."""
        # Setup mocks
        mock_logger = MagicMock()
        mock_setup_logging.return_value = mock_logger
        
        mock_mcp_instance = MagicMock()
        mock_fastmcp.return_value = mock_mcp_instance
        
        # Make run method raise an exception
        mock_mcp_instance.run.side_effect = Exception("Server run failed")
        
        # Call main function and expect it to raise the exception
        with pytest.raises(Exception, match="Server run failed"):
            main()
        
        # Verify error was logged
        mock_logger.error.assert_called_with("Failed to start MCP server: Server run failed")


class TestEnvironmentVariables:
    """Test environment variable handling."""
    
    @patch('main.FastMCP')
    @patch('main.setup_logging')
    @patch.dict(os.environ, {
        'PORT': 'invalid_port'
    })
    def test_main_invalid_port(self, mock_setup_logging, mock_fastmcp):
        """Test main function with invalid port number."""
        # Setup mocks
        mock_logger = MagicMock()
        mock_setup_logging.return_value = mock_logger
        
        mock_mcp_instance = MagicMock()
        mock_fastmcp.return_value = mock_mcp_instance
        
        # Call main function and expect ValueError for invalid port
        with pytest.raises(ValueError):
            main()
    
    @patch('main.FastMCP')
    @patch('main.setup_logging')
    @patch.dict(os.environ, {
        'DEBUG': 'invalid_debug'
    })
    def test_main_invalid_debug_value(self, mock_setup_logging, mock_fastmcp):
        """Test main function with invalid debug value."""
        # Setup mocks
        mock_logger = MagicMock()
        mock_setup_logging.return_value = mock_logger
        
        mock_mcp_instance = MagicMock()
        mock_fastmcp.return_value = mock_mcp_instance
        
        # Call main function - should handle invalid debug value gracefully
        main()
        
        # Verify setup_logging was called with debug=False (default for invalid value)
        mock_setup_logging.assert_called_once_with(False)

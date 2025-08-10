# MCP Server using Python, FastMCP and Render Boilerplate

A Model Context Protocol (MCP) server built with Python, FastMCP, designed to be deployed on Render.

## Features

- FastMCP-based MCP server implementation
- Ready for deployment on Render
- Python-based with modern async support
- Comprehensive tool integration
- Easy configuration and setup

## Quick Start

### Prerequisites

- Python 3.11.12+
- pip
- Git

### Local Development

1. Clone the repository:
```bash
git clone <your-repo-url>
cd mcp-server-using-py-fastmcp-render-boilerplate
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the server locally:
```bash
python main.py
```

### Environment Variables

Create a `.env` file in the root directory:

```env
# Server Configuration
HOST=0.0.0.0
PORT=10000
DEBUG=false

# MCP Configuration
MCP_SERVER_NAME=my-mcp-server

# Add your custom environment variables here
```

## Project Structure

```
mcp-server-using-py-fastmcp-render-boilerplate/
├── main.py                 # Main server entry point with logging
├── requirements.txt        # Python dependencies (minimal FastMCP setup)
├── env.example             # Example environment variables
├── .gitignore             # Git ignore rules
├── README.md              # This file
├── LICENSE                # MIT License
├── mcp_server.log         # Server log file (generated at runtime)
└── src/                   # Source code
    ├── __init__.py
    └── tools/             # Custom MCP tools
        ├── __init__.py
        └── example_tools.py  # Echo and calculator tools with logging
```

### Testing

Make use of the MCP Inspector Tool to test your server: https://github.com/modelcontextprotocol/inspector

## Deployment on Render

This project can be deployed on Render:

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Use the following settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Environment**: Python 3
   - **MCP_SERVER_NAME**: `my-mcp-server` (as configured in env.example)
   - **HOST**: `0.0.0.0`
   - **PORT**: 10000
   - **DEBUG**: false 

## Development

### Adding New Tools

1. Add a new tool to `src/tools/example_tools.py`
2. Implement your tool following the FastMCP pattern
3. Register the tool in `main.py`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions, please open an issue on GitHub.

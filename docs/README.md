# Playwright MCP Server

A Model Context Protocol (MCP) server that provides browser automation capabilities using Playwright. This server allows AI assistants to interact with web pages, take screenshots, fill forms, click elements, and perform various browser automation tasks.

## Features

- **Browser Navigation**: Navigate to URLs, go back/forward, reload pages
- **Element Interaction**: Click elements, type text, select options, check/uncheck boxes
- **Content Extraction**: Get text content, page titles, URLs, element attributes
- **Screenshots**: Capture full page or viewport screenshots
- **Tab Management**: Open, close, and switch between browser tabs
- **JavaScript Execution**: Evaluate custom JavaScript in the browser context
- **Wait Operations**: Wait for elements to appear/disappear or specific load states
- **Form Automation**: Fill forms, select dropdowns, handle checkboxes

## Installation

### Prerequisites

- Python 3.8 or higher
- Node.js (for Playwright browser installation)

### Install from PyPI

```bash
pip install playwright-mcp-server
```

### Install from Source

```bash
git clone https://github.com/nolecram/Build_MCP_Server.git
cd Build_MCP_Server
pip install -e .
```

### Install Playwright Browsers

After installation, you need to install the Playwright browser engines:

```bash
playwright install chromium
```

## Usage

### As an MCP Server

The server can be run as a standalone MCP server:

```bash
playwright-mcp-server
```

### Configuration for MCP Clients

Add the following configuration to your MCP client:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "playwright-mcp-server",
      "args": []
    }
  }
}
```

### VSCode Integration

To install this MCP server in VSCode with the MCP extension:

[![Install MCP Server](https://img.shields.io/badge/Install%20MCP%20Server-VSCode-blue?style=for-the-badge&logo=visualstudiocode)](vscode:extension/modelcontextprotocol.mcp)

Or manually add to your MCP configuration in VSCode settings:

```json
{
  "mcp.servers": {
    "playwright": {
      "command": "playwright-mcp-server"
    }
  }
}
```

## Available Tools

### Navigation Tools

- **browser_navigate**: Navigate to a URL
  ```json
  {"url": "https://example.com"}
  ```

- **browser_get_url**: Get the current page URL
- **browser_get_title**: Get the current page title
- **browser_go_back**: Navigate back in browser history
- **browser_go_forward**: Navigate forward in browser history
- **browser_reload**: Reload the current page

### Element Interaction Tools

- **browser_click**: Click on an element
  ```json
  {"selector": "#submit-button", "timeout": 5000}
  ```

- **browser_type**: Type text into an element
  ```json
  {"selector": "#username", "text": "user@example.com", "timeout": 5000}
  ```

- **browser_select_option**: Select an option from a dropdown
  ```json
  {"selector": "#country", "value": "US", "timeout": 5000}
  ```

- **browser_check_checkbox**: Check a checkbox
  ```json
  {"selector": "#agree-terms", "timeout": 5000}
  ```

- **browser_hover**: Hover over an element
  ```json
  {"selector": ".dropdown-trigger", "timeout": 5000}
  ```

### Content Extraction Tools

- **browser_get_text**: Get text content from an element
  ```json
  {"selector": ".error-message", "timeout": 5000}
  ```

- **browser_get_attribute**: Get an attribute value from an element
  ```json
  {"selector": "#data-field", "attribute": "data-value", "timeout": 5000}
  ```

- **browser_screenshot**: Take a screenshot
  ```json
  {"path": "/tmp/screenshot.png", "full_page": true}
  ```

### Wait and State Tools

- **browser_wait_for_selector**: Wait for an element to appear
  ```json
  {"selector": ".loading-complete", "timeout": 30000, "state": "visible"}
  ```

- **browser_wait_for_load_state**: Wait for a specific load state
  ```json
  {"state": "networkidle"}
  ```

### Tab Management Tools

- **browser_new_tab**: Open a new browser tab
  ```json
  {"url": "https://example.com"}
  ```

- **browser_close_tab**: Close the current tab

### JavaScript Execution

- **browser_evaluate**: Execute JavaScript in the browser
  ```json
  {"script": "document.querySelector('#result').textContent"}
  ```

## Examples

### Basic Web Scraping

```python
# Navigate to a website
{"tool": "browser_navigate", "arguments": {"url": "https://example.com"}}

# Wait for content to load
{"tool": "browser_wait_for_selector", "arguments": {"selector": ".content"}}

# Extract text content
{"tool": "browser_get_text", "arguments": {"selector": ".content"}}

# Take a screenshot
{"tool": "browser_screenshot", "arguments": {"full_page": true}}
```

### Form Automation

```python
# Navigate to a form
{"tool": "browser_navigate", "arguments": {"url": "https://example.com/form"}}

# Fill in form fields
{"tool": "browser_type", "arguments": {"selector": "#name", "text": "John Doe"}}
{"tool": "browser_type", "arguments": {"selector": "#email", "text": "john@example.com"}}

# Select from dropdown
{"tool": "browser_select_option", "arguments": {"selector": "#country", "value": "US"}}

# Check a checkbox
{"tool": "browser_check_checkbox", "arguments": {"selector": "#subscribe"}}

# Submit the form
{"tool": "browser_click", "arguments": {"selector": "#submit"}}
```

### Multi-tab Workflow

```python
# Open a new tab
{"tool": "browser_new_tab", "arguments": {"url": "https://example.com/page1"}}

# Work in the new tab
{"tool": "browser_get_title", "arguments": {}}

# Open another tab
{"tool": "browser_new_tab", "arguments": {"url": "https://example.com/page2"}}

# Close current tab
{"tool": "browser_close_tab", "arguments": {}}
```

## Development

### Setting up Development Environment

```bash
# Clone the repository
git clone https://github.com/nolecram/Build_MCP_Server.git
cd Build_MCP_Server

# Install in development mode
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt

# Install Playwright browsers
playwright install chromium
```

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=playwright_mcp_server

# Run specific test file
pytest tests/test_tools.py
```

### Code Formatting

```bash
# Format code with black
black src/ tests/

# Sort imports
isort src/ tests/

# Run linting
flake8 src/ tests/
```

## Architecture

The MCP server consists of several key components:

- **server.py**: Main MCP server implementation that handles protocol communication
- **tools.py**: Collection of Playwright automation tools
- **main.py**: Entry point and CLI interface

### Tool Registration

Tools are automatically registered with the MCP server and exposed through the protocol. Each tool includes:

- **Name**: Unique identifier for the tool
- **Description**: Human-readable description of what the tool does
- **Input Schema**: JSON schema defining the expected parameters
- **Implementation**: Async function that performs the actual browser automation

### Browser Management

The server manages a single browser instance with multiple contexts and pages:

- **Browser**: Single Chromium browser instance (headless by default)
- **Context**: Browser context for isolation
- **Pages**: Multiple tabs/pages within the context

## Error Handling

The server includes comprehensive error handling:

- **Network timeouts**: Configurable timeouts for network operations
- **Element not found**: Graceful handling when elements don't exist
- **Browser crashes**: Automatic cleanup and error reporting
- **Invalid selectors**: Clear error messages for malformed CSS selectors

## Security Considerations

- **Headless mode**: Runs in headless mode by default for security
- **Isolated contexts**: Each session uses isolated browser contexts
- **Resource cleanup**: Automatic cleanup of browser resources
- **Timeout limits**: Reasonable timeout limits to prevent hanging operations

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for your changes
5. Run the test suite (`pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### Version 0.1.0
- Initial implementation of Playwright MCP Server
- Support for basic browser automation tools
- Tab management capabilities
- Screenshot functionality
- Form automation tools
- JavaScript execution support
- Comprehensive test suite
- Documentation and examples
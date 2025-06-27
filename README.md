# Playwright MCP Server

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP Server](https://img.shields.io/badge/MCP-Server-green.svg)](https://modelcontextprotocol.com/)

A powerful Model Context Protocol (MCP) server that provides comprehensive browser automation capabilities using Playwright. This server enables AI assistants to interact with web pages, perform automated testing, web scraping, and complex browser-based workflows.

## 🚀 Quick Install for VSCode

Install this MCP server directly in VSCode with one click:

[![Install in VSCode](https://img.shields.io/badge/Install%20MCP%20Server-VSCode-0078d4?style=for-the-badge&logo=visualstudiocode&logoColor=white)](vscode:extension/modelcontextprotocol.mcp)

## ✨ Features

- 🌐 **Complete Browser Control**: Navigate, click, type, and interact with any web element
- 📸 **Screenshot & Visual Testing**: Capture full pages or specific elements
- 🔄 **Tab Management**: Open, close, and switch between multiple browser tabs
- 📝 **Form Automation**: Fill forms, select options, handle checkboxes and radio buttons
- ⏳ **Smart Waiting**: Wait for elements, network requests, or specific page states
- 🔍 **Content Extraction**: Get text, attributes, and data from web pages
- 💻 **JavaScript Execution**: Run custom JavaScript in the browser context
- 🛡️ **Robust Error Handling**: Comprehensive error handling with meaningful messages

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- Node.js (required for Playwright browser installation)

### Install from PyPI

```bash
pip install playwright-mcp-server
playwright install chromium
```

### Install from Source

```bash
git clone https://github.com/nolecram/Build_MCP_Server.git
cd Build_MCP_Server
pip install -e .
playwright install chromium
```

## 🔧 Configuration

### For MCP Clients

Add to your MCP client configuration:

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

### For VSCode MCP Extension

Add to your VSCode settings:

```json
{
  "mcp.servers": {
    "playwright": {
      "command": "playwright-mcp-server"
    }
  }
}
```

## 🛠️ Available Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `browser_navigate` | Navigate to a URL | `url` |
| `browser_click` | Click on an element | `selector`, `timeout?` |
| `browser_type` | Type text into an element | `selector`, `text`, `timeout?` |
| `browser_screenshot` | Take a screenshot | `path?`, `full_page?` |
| `browser_get_text` | Extract text from an element | `selector`, `timeout?` |
| `browser_wait_for_selector` | Wait for element to appear | `selector`, `timeout?`, `state?` |
| `browser_evaluate` | Execute JavaScript | `script` |
| `browser_new_tab` | Open a new tab | `url?` |
| `browser_close_tab` | Close current tab | - |
| `browser_get_title` | Get page title | - |
| `browser_get_url` | Get current URL | - |

## 💡 Usage Examples

### Web Scraping
```bash
# Navigate to a website
browser_navigate {"url": "https://example.com"}

# Wait for content to load
browser_wait_for_selector {"selector": ".content"}

# Extract information
browser_get_text {"selector": ".price"}

# Take a screenshot
browser_screenshot {"full_page": true}
```

### Form Automation
```bash
# Fill out a form
browser_type {"selector": "#email", "text": "user@example.com"}
browser_type {"selector": "#password", "text": "secretpassword"}
browser_click {"selector": "#login-button"}
```

### Testing Workflows
```bash
# Multi-step testing
browser_navigate {"url": "https://app.example.com"}
browser_click {"selector": "#feature-button"}
browser_wait_for_selector {"selector": ".success-message"}
browser_screenshot {"path": "test-result.png"}
```

## 🧪 Testing

Run the test suite:

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest tests/

# Run with coverage
pytest --cov=playwright_mcp_server tests/
```

## 📚 Documentation

Comprehensive documentation is available in the [docs](docs/) directory:

- [API Reference](docs/README.md)
- [Tool Specifications](docs/README.md#available-tools)
- [Examples and Tutorials](docs/README.md#examples)

## 🔒 Security

- Runs in headless mode by default
- Isolated browser contexts for each session
- Automatic resource cleanup
- Configurable timeout limits
- No sensitive data logging

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch
3. Add tests for your changes
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Playwright](https://playwright.dev/) for reliable browser automation
- Implements the [Model Context Protocol](https://modelcontextprotocol.com/) specification
- Inspired by the need for robust browser automation in AI workflows

## 📈 Roadmap

- [ ] Support for multiple browser engines (Firefox, Safari)
- [ ] Advanced element selection strategies
- [ ] Built-in visual regression testing
- [ ] Performance monitoring and metrics
- [ ] Browser extension interaction
- [ ] Mobile browser simulation

---

⭐ **Star this repository if you find it useful!**
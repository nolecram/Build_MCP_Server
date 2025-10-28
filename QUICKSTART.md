# Quick Start Guide

Get up and running with Playwright MCP Server in 5 minutes!

## 1. Install

```bash
# Install the package
pip install playwright-mcp-server

# Install browsers
playwright install chromium
```

## 2. Run Server

```bash
playwright-mcp-server
```

## 3. Configure Client

### Claude Desktop / MCP Extension

Add to your configuration:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "playwright-mcp-server"
    }
  }
}
```

## 4. First Test

The server is now ready to handle browser automation requests!

### Example Tasks

#### Navigate to a Website
```
Navigate to https://example.com and take a screenshot
```

#### Extract Content
```
Go to https://example.com and get all the text from the main content area
```

#### Fill a Form
```
Navigate to https://example.com/form
Fill in the name field with "John Doe"
Fill in the email field with "john@example.com"
Click the submit button
Wait for the success message
```

## 5. Development

### Setup Development Environment

```bash
# Clone repo
git clone https://github.com/nolecram/Build_MCP_Server.git
cd Build_MCP_Server

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install in dev mode
pip install -e .
pip install -r requirements-dev.txt
playwright install chromium
```

### Run Tests

```bash
pytest
```

### Format Code

```bash
black src/ tests/
isort src/ tests/
```

## 📚 Learn More

- **Full Documentation:** [docs/README.md](docs/README.md)
- **API Reference:** [docs/API.md](docs/API.md)
- **Examples:** [docs/EXAMPLES.md](docs/EXAMPLES.md)
- **Contributing:** [CONTRIBUTING.md](CONTRIBUTING.md)

## 🆘 Troubleshooting

### Browsers not found?
```bash
playwright install --with-deps
```

### Import errors?
```bash
pip install --upgrade playwright
```

### Connection refused?
Ensure the server is running:
```bash
playwright-mcp-server
```

## 🎯 Available Tools

| Tool | Purpose |
|------|----------|
| `browser_navigate` | Go to URL |
| `browser_click` | Click element |
| `browser_type` | Type text |
| `browser_screenshot` | Capture screen |
| `browser_get_text` | Extract text |
| `browser_wait_for_selector` | Wait for element |
| `browser_evaluate` | Run JavaScript |
| `browser_new_tab` | Open new tab |
| `browser_close_tab` | Close tab |

See [API Reference](docs/API.md) for complete list.

## 🚀 Pro Tips

1. **Use descriptive selectors** - CSS selectors work best (e.g., `.button`, `#submit`)
2. **Set appropriate timeouts** - Default is 5-30 seconds, adjust as needed
3. **Chain operations** - Multiple operations on single page are more efficient
4. **Handle errors gracefully** - All methods return descriptive error messages

## ❓ Need Help?

- Check [CONTRIBUTING.md](CONTRIBUTING.md) for development help
- Review [docs/EXAMPLES.md](docs/EXAMPLES.md) for common patterns
- Search [GitHub Issues](https://github.com/nolecram/Build_MCP_Server/issues)

---

**Happy automating!** 🎉
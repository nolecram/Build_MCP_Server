# API Reference

## PlaywrightMCPServer

Main server class that implements the MCP protocol for Playwright browser automation.

### Methods

#### `__init__()`
Initialize the Playwright MCP Server.

#### `run()`
Start the MCP server and begin listening for requests.

#### `cleanup()`
Clean up browser resources and stop the server.

## PlaywrightTools

Collection of browser automation tools available through the MCP server.

### Navigation Methods

#### `navigate(page: Page, url: str) -> str`
Navigate to a specific URL.

**Parameters:**
- `page`: Playwright page instance
- `url`: Target URL to navigate to

**Returns:**
- Success/error message string

#### `get_url(page: Page) -> str`
Get the current page URL.

#### `get_title(page: Page) -> str`
Get the current page title.

### Element Interaction Methods

#### `click(page: Page, selector: str, timeout: int = 5000) -> str`
Click on an element matching the selector.

**Parameters:**
- `page`: Playwright page instance
- `selector`: CSS selector for the target element
- `timeout`: Maximum wait time in milliseconds

#### `type_text(page: Page, selector: str, text: str, timeout: int = 5000) -> str`
Type text into an input element.

**Parameters:**
- `page`: Playwright page instance
- `selector`: CSS selector for the input element
- `text`: Text to type
- `timeout`: Maximum wait time in milliseconds

#### `select_option(page: Page, selector: str, value: str, timeout: int = 5000) -> str`
Select an option from a dropdown.

### Content Extraction Methods

#### `get_text(page: Page, selector: str, timeout: int = 5000) -> str`
Extract text content from an element.

#### `get_attribute(page: Page, selector: str, attribute: str, timeout: int = 5000) -> str`
Get an attribute value from an element.

#### `screenshot(page: Page, path: Optional[str] = None, full_page: bool = False) -> str`
Take a screenshot of the page.

### Wait Methods

#### `wait_for_selector(page: Page, selector: str, timeout: int = 30000, state: str = "visible") -> str`
Wait for an element to reach a specific state.

**Parameters:**
- `state`: One of "visible", "hidden", "attached", "detached"

#### `wait_for_load_state(page: Page, state: str = "load") -> str`
Wait for a specific load state.

**Parameters:**
- `state`: One of "load", "domcontentloaded", "networkidle"

### JavaScript Methods

#### `evaluate(page: Page, script: str) -> str`
Execute JavaScript code in the browser context.

## Error Handling

All methods return string results that indicate success or failure. Errors are caught and returned as descriptive error messages rather than raising exceptions.

## Browser Management

The server automatically manages:
- Browser instance lifecycle
- Page/tab creation and cleanup  
- Context isolation
- Resource cleanup on shutdown
# Examples

## Web Scraping Example

Extract product information from an e-commerce site:

```json
{
  "tool": "browser_navigate",
  "arguments": {"url": "https://example-shop.com/products"}
}

{
  "tool": "browser_wait_for_selector", 
  "arguments": {"selector": ".product-list"}
}

{
  "tool": "browser_get_text",
  "arguments": {"selector": ".product-title"}
}

{
  "tool": "browser_get_text", 
  "arguments": {"selector": ".product-price"}
}

{
  "tool": "browser_screenshot",
  "arguments": {"path": "product-page.png", "full_page": true}
}
```

## Form Automation Example

Fill out and submit a contact form:

```json
{
  "tool": "browser_navigate",
  "arguments": {"url": "https://example.com/contact"}
}

{
  "tool": "browser_type",
  "arguments": {"selector": "#name", "text": "John Doe"}
}

{
  "tool": "browser_type", 
  "arguments": {"selector": "#email", "text": "john@example.com"}
}

{
  "tool": "browser_type",
  "arguments": {"selector": "#message", "text": "Hello, I'm interested in your services."}
}

{
  "tool": "browser_select_option",
  "arguments": {"selector": "#subject", "value": "general-inquiry"}
}

{
  "tool": "browser_check_checkbox",
  "arguments": {"selector": "#newsletter"}
}

{
  "tool": "browser_click",
  "arguments": {"selector": "#submit-button"}
}

{
  "tool": "browser_wait_for_selector",
  "arguments": {"selector": ".success-message"}
}
```

## Multi-Tab Workflow Example

Work with multiple tabs simultaneously:

```json
{
  "tool": "browser_navigate",
  "arguments": {"url": "https://docs.example.com"}
}

{
  "tool": "browser_new_tab",
  "arguments": {"url": "https://api.example.com"}
}

{
  "tool": "browser_get_text",
  "arguments": {"selector": ".api-key"}
}

{
  "tool": "browser_new_tab", 
  "arguments": {"url": "https://app.example.com/settings"}
}

{
  "tool": "browser_type",
  "arguments": {"selector": "#api-key-input", "text": "retrieved-api-key"}
}

{
  "tool": "browser_click",
  "arguments": {"selector": "#save-settings"}
}

{
  "tool": "browser_close_tab",
  "arguments": {}}
```

## Testing Workflow Example

Automated UI testing:

```json
{
  "tool": "browser_navigate",
  "arguments": {"url": "https://app.example.com/login"}
}

{
  "tool": "browser_type",  
  "arguments": {"selector": "#username", "text": "testuser"}
}

{
  "tool": "browser_type",
  "arguments": {"selector": "#password", "text": "testpass123"}
}

{
  "tool": "browser_click",
  "arguments": {"selector": "#login-btn"}}

{
  "tool": "browser_wait_for_selector",
  "arguments": {"selector": ".dashboard", "timeout": 10000}
}

{
  "tool": "browser_screenshot",
  "arguments": {"path": "dashboard-loaded.png"}
}

{
  "tool": "browser_click",
  "arguments": {"selector": "#new-project-btn"}
}

{
  "tool": "browser_wait_for_selector",
  "arguments": {"selector": "#project-form"}
}

{
  "tool": "browser_type",
  "arguments": {"selector": "#project-name", "text": "Test Project"}
}

{
  "tool": "browser_click", 
  "arguments": {"selector": "#create-project"}}

{
  "tool": "browser_wait_for_selector",
  "arguments": {"selector": ".project-created-success"}}
```

## Data Extraction Example

Extract structured data from a table:

```json
{
  "tool": "browser_navigate",
  "arguments": {"url": "https://example.com/data-table"}
}

{
  "tool": "browser_wait_for_selector",
  "arguments": {"selector": "table.data-table"}}

{
  "tool": "browser_evaluate",
  "arguments": {
    "script": "Array.from(document.querySelectorAll('table.data-table tr')).map(row => Array.from(row.querySelectorAll('td')).map(cell => cell.textContent.trim()))"
  }
}

{
  "tool": "browser_get_attribute",
  "arguments": {"selector": "table.data-table", "attribute": "data-total-rows"}
}
```

## File Upload Example

Upload files through a web form:

```json
{
  "tool": "browser_navigate", 
  "arguments": {"url": "https://example.com/upload"}
}

{
  "tool": "browser_evaluate",
  "arguments": {
    "script": "document.querySelector('#file-input').files = new FileList(); document.querySelector('#file-input').dispatchEvent(new Event('change'));"
  }
}

{
  "tool": "browser_click",
  "arguments": {"selector": "#upload-button"}}

{
  "tool": "browser_wait_for_selector",
  "arguments": {"selector": ".upload-success"}}
```

## Dynamic Content Example

Handle dynamically loaded content:

```json
{
  "tool": "browser_navigate",
  "arguments": {"url": "https://spa-example.com"}}

{
  "tool": "browser_wait_for_load_state",
  "arguments": {"state": "networkidle"}}

{
  "tool": "browser_click",
  "arguments": {"selector": ".load-more-btn"}}

{
  "tool": "browser_wait_for_selector", 
  "arguments": {"selector": ".new-content", "timeout": 15000}}

{
  "tool": "browser_evaluate",
  "arguments": {
    "script": "window.scrollTo(0, document.body.scrollHeight)"
  }}

{
  "tool": "browser_wait_for_selector",
  "arguments": {"selector": ".footer-loaded"}}
```
"""Core MCP Server implementation for Playwright browser automation."""

import asyncio
import json
import logging
import sys
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
import traceback

from mcp import types
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from playwright.async_api import async_playwright, Browser, BrowserContext, Page, Playwright
from pydantic import BaseModel

from playwright_mcp_server.tools import PlaywrightTools


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PlaywrightMCPServer:
    """Main MCP Server class for Playwright browser automation."""
    
    def __init__(self) -> None:
        """Initialize the Playwright MCP Server."""
        self.server = Server("playwright-mcp-server")
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.pages: List[Page] = []
        self.current_page: Optional[Page] = None
        self.tools = PlaywrightTools()
        
        # Register handlers
        self._register_handlers()
    
    def _register_handlers(self) -> None:
        """Register MCP protocol handlers."""
        
        @self.server.list_tools()
        async def handle_list_tools() -> list[types.Tool]:
            """List available tools."""
            return [
                types.Tool(
                    name="browser_navigate",
                    description="Navigate to a URL",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "The URL to navigate to"
                            }
                        },
                        "required": ["url"]
                    }
                ),
                types.Tool(
                    name="browser_click",
                    description="Click on an element",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "selector": {
                                "type": "string",
                                "description": "CSS selector for the element to click"
                            },
                            "timeout": {
                                "type": "number",
                                "description": "Timeout in milliseconds",
                                "default": 5000
                            }
                        },
                        "required": ["selector"]
                    }
                ),
                types.Tool(
                    name="browser_type",
                    description="Type text into an element",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "selector": {
                                "type": "string",
                                "description": "CSS selector for the element to type into"
                            },
                            "text": {
                                "type": "string",
                                "description": "Text to type"
                            },
                            "timeout": {
                                "type": "number",
                                "description": "Timeout in milliseconds",
                                "default": 5000
                            }
                        },
                        "required": ["selector", "text"]
                    }
                ),
                types.Tool(
                    name="browser_screenshot",
                    description="Take a screenshot of the current page",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Path to save the screenshot (optional)"
                            },
                            "full_page": {
                                "type": "boolean",
                                "description": "Whether to capture the full scrollable page",
                                "default": False
                            }
                        }
                    }
                ),
                types.Tool(
                    name="browser_get_text",
                    description="Get text content from an element",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "selector": {
                                "type": "string",
                                "description": "CSS selector for the element"
                            },
                            "timeout": {
                                "type": "number",
                                "description": "Timeout in milliseconds",
                                "default": 5000
                            }
                        },
                        "required": ["selector"]
                    }
                ),
                types.Tool(
                    name="browser_wait_for_selector",
                    description="Wait for an element to appear",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "selector": {
                                "type": "string",
                                "description": "CSS selector to wait for"
                            },
                            "timeout": {
                                "type": "number",
                                "description": "Timeout in milliseconds",
                                "default": 30000
                            },
                            "state": {
                                "type": "string",
                                "description": "State to wait for (visible, hidden, attached, detached)",
                                "default": "visible"
                            }
                        },
                        "required": ["selector"]
                    }
                ),
                types.Tool(
                    name="browser_evaluate",
                    description="Evaluate JavaScript in the browser",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "script": {
                                "type": "string",
                                "description": "JavaScript code to execute"
                            }
                        },
                        "required": ["script"]
                    }
                ),
                types.Tool(
                    name="browser_new_tab",
                    description="Open a new browser tab",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "URL to open in the new tab (optional)"
                            }
                        }
                    }
                ),
                types.Tool(
                    name="browser_close_tab",
                    description="Close the current tab",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                types.Tool(
                    name="browser_get_title",
                    description="Get the title of the current page",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                types.Tool(
                    name="browser_get_url",
                    description="Get the URL of the current page",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                types.Tool(
                    name="browser_select_option",
                    description="Select an option from a dropdown",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "selector": {
                                "type": "string",
                                "description": "CSS selector for the dropdown element"
                            },
                            "value": {
                                "type": "string",
                                "description": "Value to select"
                            },
                            "timeout": {
                                "type": "number",
                                "description": "Timeout in milliseconds",
                                "default": 5000
                            }
                        },
                        "required": ["selector", "value"]
                    }
                ),
                types.Tool(
                    name="browser_check_checkbox",
                    description="Check a checkbox",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "selector": {
                                "type": "string",
                                "description": "CSS selector for the checkbox"
                            },
                            "timeout": {
                                "type": "number",
                                "description": "Timeout in milliseconds",
                                "default": 5000
                            }
                        },
                        "required": ["selector"]
                    }
                ),
                types.Tool(
                    name="browser_uncheck_checkbox",
                    description="Uncheck a checkbox",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "selector": {
                                "type": "string",
                                "description": "CSS selector for the checkbox"
                            },
                            "timeout": {
                                "type": "number",
                                "description": "Timeout in milliseconds",
                                "default": 5000
                            }
                        },
                        "required": ["selector"]
                    }
                ),
                types.Tool(
                    name="browser_hover",
                    description="Hover over an element",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "selector": {
                                "type": "string",
                                "description": "CSS selector for the element to hover over"
                            },
                            "timeout": {
                                "type": "number",
                                "description": "Timeout in milliseconds",
                                "default": 5000
                            }
                        },
                        "required": ["selector"]
                    }
                ),
                types.Tool(
                    name="browser_scroll_to",
                    description="Scroll to an element",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "selector": {
                                "type": "string",
                                "description": "CSS selector for the element to scroll to"
                            },
                            "timeout": {
                                "type": "number",
                                "description": "Timeout in milliseconds",
                                "default": 5000
                            }
                        },
                        "required": ["selector"]
                    }
                ),
                types.Tool(
                    name="browser_get_attribute",
                    description="Get an attribute value from an element",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "selector": {
                                "type": "string",
                                "description": "CSS selector for the element"
                            },
                            "attribute": {
                                "type": "string",
                                "description": "Name of the attribute to get"
                            },
                            "timeout": {
                                "type": "number",
                                "description": "Timeout in milliseconds",
                                "default": 5000
                            }
                        },
                        "required": ["selector", "attribute"]
                    }
                ),
                types.Tool(
                    name="browser_wait_for_load_state",
                    description="Wait for a specific load state",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "state": {
                                "type": "string",
                                "description": "Load state to wait for (load, domcontentloaded, networkidle)",
                                "default": "load"
                            }
                        }
                    }
                ),
                types.Tool(
                    name="browser_go_back",
                    description="Go back in browser history",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                types.Tool(
                    name="browser_go_forward",
                    description="Go forward in browser history",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                types.Tool(
                    name="browser_reload",
                    description="Reload the current page",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                types.Tool(
                    name="browser_fill_form",
                    description="Fill multiple form fields and optionally submit",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "form_data": {
                                "type": "object",
                                "description": "Key-value pairs where key is CSS selector and value is text to fill",
                                "additionalProperties": {"type": "string"}
                            },
                            "submit_selector": {
                                "type": "string",
                                "description": "CSS selector for submit button (optional)"
                            }
                        },
                        "required": ["form_data"]
                    }
                ),
                types.Tool(
                    name="browser_get_links",
                    description="Get all links on the current page",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "number",
                                "description": "Maximum number of links to return",
                                "default": 50
                            }
                        }
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(
            name: str, arguments: dict[str, Any] | None
        ) -> list[types.TextContent]:
            """Handle tool calls."""
            try:
                # Validate arguments first
                arguments = self._validate_arguments(name, arguments)
                
                # Ensure browser is initialized
                await self._ensure_browser()
                
                if not self.current_page:
                    return [types.TextContent(type="text", text="No active page available")]
                
                if name == "browser_navigate":
                    result = await self.tools.navigate(self.current_page, arguments.get("url"))
                elif name == "browser_click":
                    result = await self.tools.click(
                        self.current_page, 
                        arguments.get("selector"),
                        arguments.get("timeout", 5000)
                    )
                elif name == "browser_type":
                    result = await self.tools.type_text(
                        self.current_page,
                        arguments.get("selector"),
                        arguments.get("text"),
                        arguments.get("timeout", 5000)
                    )
                elif name == "browser_screenshot":
                    result = await self.tools.screenshot(
                        self.current_page,
                        arguments.get("path"),
                        arguments.get("full_page", False)
                    )
                elif name == "browser_get_text":
                    result = await self.tools.get_text(
                        self.current_page,
                        arguments.get("selector"),
                        arguments.get("timeout", 5000)
                    )
                elif name == "browser_wait_for_selector":
                    result = await self.tools.wait_for_selector(
                        self.current_page,
                        arguments.get("selector"),
                        arguments.get("timeout", 30000),
                        arguments.get("state", "visible")
                    )
                elif name == "browser_evaluate":
                    result = await self.tools.evaluate(
                        self.current_page,
                        arguments.get("script")
                    )
                elif name == "browser_new_tab":
                    result = await self._new_tab(arguments.get("url"))
                elif name == "browser_close_tab":
                    result = await self._close_tab()
                elif name == "browser_get_title":
                    result = await self.tools.get_title(self.current_page)
                elif name == "browser_get_url":
                    result = await self.tools.get_url(self.current_page)
                elif name == "browser_select_option":
                    result = await self.tools.select_option(
                        self.current_page,
                        arguments.get("selector"),
                        arguments.get("value"),
                        arguments.get("timeout", 5000)
                    )
                elif name == "browser_check_checkbox":
                    result = await self.tools.check_checkbox(
                        self.current_page,
                        arguments.get("selector"),
                        arguments.get("timeout", 5000)
                    )
                elif name == "browser_uncheck_checkbox":
                    result = await self.tools.uncheck_checkbox(
                        self.current_page,
                        arguments.get("selector"),
                        arguments.get("timeout", 5000)
                    )
                elif name == "browser_hover":
                    result = await self.tools.hover(
                        self.current_page,
                        arguments.get("selector"),
                        arguments.get("timeout", 5000)
                    )
                elif name == "browser_scroll_to":
                    result = await self.tools.scroll_to(
                        self.current_page,
                        arguments.get("selector"),
                        arguments.get("timeout", 5000)
                    )
                elif name == "browser_get_attribute":
                    result = await self.tools.get_attribute(
                        self.current_page,
                        arguments.get("selector"),
                        arguments.get("attribute"),
                        arguments.get("timeout", 5000)
                    )
                elif name == "browser_wait_for_load_state":
                    result = await self.tools.wait_for_load_state(
                        self.current_page,
                        arguments.get("state", "load")
                    )
                elif name == "browser_go_back":
                    result = await self.tools.go_back(self.current_page)
                elif name == "browser_go_forward":
                    result = await self.tools.go_forward(self.current_page)
                elif name == "browser_reload":
                    result = await self.tools.reload(self.current_page)
                elif name == "browser_fill_form":
                    form_data = arguments.get("form_data", {})
                    submit_selector = arguments.get("submit_selector")
                    result = await self.tools.fill_form(self.current_page, form_data, submit_selector)
                elif name == "browser_get_links":
                    limit = arguments.get("limit", 50)
                    result = await self.tools.get_links(self.current_page, limit)
                else:
                    result = f"Unknown tool: {name}"
                
                return [types.TextContent(type="text", text=str(result))]
            
            except Exception as e:
                error_msg = f"Error executing {name}: {str(e)}\n{traceback.format_exc()}"
                logger.error(error_msg)
                return [types.TextContent(type="text", text=error_msg)]
    
    def _validate_arguments(self, name: str, arguments: dict[str, Any] | None) -> dict[str, Any]:
        """Validate and sanitize tool arguments."""
        if arguments is None:
            arguments = {}
        
        # Basic validation for common parameters
        if "timeout" in arguments:
            timeout = arguments.get("timeout")
            if not isinstance(timeout, (int, float)) or timeout <= 0:
                arguments["timeout"] = 5000  # Default timeout
            elif timeout > 60000:  # Cap at 60 seconds
                arguments["timeout"] = 60000
        
        if "selector" in arguments:
            selector = arguments.get("selector")
            if not isinstance(selector, str) or not selector.strip():
                raise ValueError("Selector must be a non-empty string")
            arguments["selector"] = selector.strip()
        
        if "url" in arguments:
            url = arguments.get("url")
            if not isinstance(url, str) or not url.strip():
                raise ValueError("URL must be a non-empty string")
            # Basic URL validation
            if not (url.startswith("http://") or url.startswith("https://") or url.startswith("file://")):
                raise ValueError("URL must start with http://, https://, or file://")
        
        if "text" in arguments:
            text = arguments.get("text")
            if not isinstance(text, str):
                raise ValueError("Text must be a string")
        
        if "script" in arguments:
            script = arguments.get("script")
            if not isinstance(script, str) or not script.strip():
                raise ValueError("Script must be a non-empty string")
        
        if "form_data" in arguments:
            form_data = arguments.get("form_data")
            if not isinstance(form_data, dict):
                raise ValueError("Form data must be a dictionary")
            for key, value in form_data.items():
                if not isinstance(key, str) or not key.strip():
                    raise ValueError("Form data keys must be non-empty strings (CSS selectors)")
                if not isinstance(value, str):
                    raise ValueError("Form data values must be strings")
        
        return arguments

    async def _ensure_browser(self) -> None:
        """Ensure browser is initialized."""
        if not self.playwright:
            self.playwright = await async_playwright().start()
        
        if not self.browser:
            # Launch with optimized settings for MCP server use
            self.browser = await self.playwright.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage",  # Overcome limited resource problems
                    "--disable-gpu",
                    "--no-first-run",
                    "--disable-default-apps",
                    "--disable-features=TranslateUI",
                    "--disable-ipc-flooding-protection"
                ]
            )
        
        if not self.context:
            # Create context with reasonable defaults
            self.context = await self.browser.new_context(
                viewport={"width": 1280, "height": 720},
                user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
        
        if not self.current_page:
            self.current_page = await self.context.new_page()
            self.pages.append(self.current_page)
    
    async def _new_tab(self, url: Optional[str] = None) -> str:
        """Open a new tab."""
        try:
            if not self.context:
                await self._ensure_browser()
            
            page = await self.context.new_page()
            self.pages.append(page)
            self.current_page = page
            
            if url:
                result = await self.tools.navigate(page, url)
                if "Successfully" in result:
                    return f"New tab opened and navigated to: {url}"
                else:
                    return f"New tab opened but navigation failed: {result}"
            else:
                return f"New tab opened (total tabs: {len(self.pages)})"
        except Exception as e:
            return f"Failed to open new tab: {str(e)}"
    
    async def _close_tab(self) -> str:
        """Close the current tab."""
        try:
            if not self.current_page:
                return "No active tab to close"
            
            if len(self.pages) <= 1:
                return "Cannot close the last tab"
            
            page_to_close = self.current_page
            self.pages.remove(page_to_close)
            self.current_page = self.pages[-1] if self.pages else None
            
            await page_to_close.close()
            
            return f"Tab closed (remaining tabs: {len(self.pages)})"
        except Exception as e:
            return f"Failed to close tab: {str(e)}"
    
    async def run(self) -> None:
        """Run the server."""
        # Use stdio transport
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="playwright-mcp-server",
                    server_version="0.1.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )
    
    async def cleanup(self) -> None:
        """Clean up resources."""
        try:
            if self.pages:
                for page in self.pages:
                    await page.close()
            
            if self.context:
                await self.context.close()
            
            if self.browser:
                await self.browser.close()
            
            if self.playwright:
                await self.playwright.stop()
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
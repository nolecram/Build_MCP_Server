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
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(
            name: str, arguments: dict[str, Any] | None
        ) -> list[types.TextContent]:
            """Handle tool calls."""
            try:
                # Ensure browser is initialized
                await self._ensure_browser()
                
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
                else:
                    result = f"Unknown tool: {name}"
                
                return [types.TextContent(type="text", text=str(result))]
            
            except Exception as e:
                error_msg = f"Error executing {name}: {str(e)}\n{traceback.format_exc()}"
                logger.error(error_msg)
                return [types.TextContent(type="text", text=error_msg)]
    
    async def _ensure_browser(self) -> None:
        """Ensure browser is initialized."""
        if not self.playwright:
            self.playwright = await async_playwright().start()
        
        if not self.browser:
            self.browser = await self.playwright.chromium.launch(headless=True)
        
        if not self.context:
            self.context = await self.browser.new_context()
        
        if not self.current_page:
            self.current_page = await self.context.new_page()
            self.pages.append(self.current_page)
    
    async def _new_tab(self, url: Optional[str] = None) -> str:
        """Open a new tab."""
        if not self.context:
            await self._ensure_browser()
        
        page = await self.context.new_page()
        self.pages.append(page)
        self.current_page = page
        
        if url:
            await page.goto(url)
            return f"New tab opened and navigated to: {url}"
        else:
            return "New tab opened"
    
    async def _close_tab(self) -> str:
        """Close the current tab."""
        if not self.current_page:
            return "No active tab to close"
        
        if len(self.pages) <= 1:
            return "Cannot close the last tab"
        
        await self.current_page.close()
        self.pages.remove(self.current_page)
        self.current_page = self.pages[-1] if self.pages else None
        
        return "Tab closed"
    
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
"""Playwright tools for browser automation."""

import asyncio
import base64
import logging
from pathlib import Path
from typing import Any, Optional, Union

from playwright.async_api import Page

logger = logging.getLogger(__name__)


class PlaywrightTools:
    """Collection of Playwright browser automation tools."""
    
    async def navigate(self, page: Page, url: str) -> str:
        """Navigate to a URL."""
        try:
            await page.goto(url, wait_until="domcontentloaded")
            return f"Successfully navigated to: {url}"
        except Exception as e:
            return f"Failed to navigate to {url}: {str(e)}"
    
    async def click(self, page: Page, selector: str, timeout: int = 5000) -> str:
        """Click on an element."""
        try:
            await page.click(selector, timeout=timeout)
            return f"Successfully clicked element: {selector}"
        except Exception as e:
            return f"Failed to click element {selector}: {str(e)}"
    
    async def type_text(self, page: Page, selector: str, text: str, timeout: int = 5000) -> str:
        """Type text into an element."""
        try:
            await page.fill(selector, text, timeout=timeout)
            return f"Successfully typed text into element: {selector}"
        except Exception as e:
            return f"Failed to type text into element {selector}: {str(e)}"
    
    async def screenshot(self, page: Page, path: Optional[str] = None, full_page: bool = False) -> str:
        """Take a screenshot of the page."""
        try:
            if path:
                await page.screenshot(path=path, full_page=full_page)
                return f"Screenshot saved to: {path}"
            else:
                # Return base64 encoded screenshot
                screenshot_bytes = await page.screenshot(full_page=full_page)
                screenshot_b64 = base64.b64encode(screenshot_bytes).decode()
                return f"Screenshot taken (base64): {screenshot_b64[:100]}..."
        except Exception as e:
            return f"Failed to take screenshot: {str(e)}"
    
    async def get_text(self, page: Page, selector: str, timeout: int = 5000) -> str:
        """Get text content from an element."""
        try:
            element = await page.wait_for_selector(selector, timeout=timeout)
            if element:
                text = await element.text_content()
                return text or ""
            return ""
        except Exception as e:
            return f"Failed to get text from element {selector}: {str(e)}"
    
    async def wait_for_selector(self, page: Page, selector: str, timeout: int = 30000, state: str = "visible") -> str:
        """Wait for an element to appear."""
        try:
            await page.wait_for_selector(selector, timeout=timeout, state=state)
            return f"Element {selector} is now {state}"
        except Exception as e:
            return f"Failed to wait for element {selector}: {str(e)}"
    
    async def evaluate(self, page: Page, script: str) -> str:
        """Evaluate JavaScript in the browser."""
        try:
            result = await page.evaluate(script)
            return str(result)
        except Exception as e:
            return f"Failed to evaluate script: {str(e)}"
    
    async def get_title(self, page: Page) -> str:
        """Get the title of the current page."""
        try:
            title = await page.title()
            return title
        except Exception as e:
            return f"Failed to get page title: {str(e)}"
    
    async def get_url(self, page: Page) -> str:
        """Get the URL of the current page."""
        try:
            url = page.url
            return url
        except Exception as e:
            return f"Failed to get page URL: {str(e)}"
    
    async def select_option(self, page: Page, selector: str, value: str, timeout: int = 5000) -> str:
        """Select an option from a dropdown."""
        try:
            await page.select_option(selector, value, timeout=timeout)
            return f"Successfully selected option '{value}' in element: {selector}"
        except Exception as e:
            return f"Failed to select option in element {selector}: {str(e)}"
    
    async def check_checkbox(self, page: Page, selector: str, timeout: int = 5000) -> str:
        """Check a checkbox."""
        try:
            await page.check(selector, timeout=timeout)
            return f"Successfully checked checkbox: {selector}"
        except Exception as e:
            return f"Failed to check checkbox {selector}: {str(e)}"
    
    async def uncheck_checkbox(self, page: Page, selector: str, timeout: int = 5000) -> str:
        """Uncheck a checkbox."""
        try:
            await page.uncheck(selector, timeout=timeout)
            return f"Successfully unchecked checkbox: {selector}"
        except Exception as e:
            return f"Failed to uncheck checkbox {selector}: {str(e)}"
    
    async def hover(self, page: Page, selector: str, timeout: int = 5000) -> str:
        """Hover over an element."""
        try:
            await page.hover(selector, timeout=timeout)
            return f"Successfully hovered over element: {selector}"
        except Exception as e:
            return f"Failed to hover over element {selector}: {str(e)}"
    
    async def scroll_to(self, page: Page, selector: str, timeout: int = 5000) -> str:
        """Scroll to an element."""
        try:
            element = await page.wait_for_selector(selector, timeout=timeout)
            if element:
                await element.scroll_into_view_if_needed()
                return f"Successfully scrolled to element: {selector}"
            return f"Element not found: {selector}"
        except Exception as e:
            return f"Failed to scroll to element {selector}: {str(e)}"
    
    async def get_attribute(self, page: Page, selector: str, attribute: str, timeout: int = 5000) -> str:
        """Get an attribute value from an element."""
        try:
            element = await page.wait_for_selector(selector, timeout=timeout)
            if element:
                value = await element.get_attribute(attribute)
                return value or ""
            return ""
        except Exception as e:
            return f"Failed to get attribute {attribute} from element {selector}: {str(e)}"
    
    async def wait_for_load_state(self, page: Page, state: str = "load") -> str:
        """Wait for a specific load state."""
        try:
            await page.wait_for_load_state(state)
            return f"Page reached load state: {state}"
        except Exception as e:
            return f"Failed to wait for load state {state}: {str(e)}"
    
    async def go_back(self, page: Page) -> str:
        """Go back in browser history."""
        try:
            await page.go_back()
            return "Successfully navigated back"
        except Exception as e:
            return f"Failed to go back: {str(e)}"
    
    async def go_forward(self, page: Page) -> str:
        """Go forward in browser history."""
        try:
            await page.go_forward()
            return "Successfully navigated forward"
        except Exception as e:
            return f"Failed to go forward: {str(e)}"
    
    async def reload(self, page: Page) -> str:
        """Reload the current page."""
        try:
            await page.reload()
            return "Successfully reloaded page"
        except Exception as e:
            return f"Failed to reload page: {str(e)}"
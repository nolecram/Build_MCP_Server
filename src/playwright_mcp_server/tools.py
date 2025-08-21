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
            # Add timeout and better error handling
            response = await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            
            if response is None:
                return f"Navigation to {url} failed: No response received"
            
            if response.status >= 400:
                return f"Navigation to {url} completed with status {response.status}"
            
            return f"Successfully navigated to: {url}"
        except Exception as e:
            error_msg = str(e)
            if "timeout" in error_msg.lower():
                return f"Navigation to {url} timed out: {error_msg}"
            elif "net::" in error_msg:
                return f"Network error navigating to {url}: {error_msg}"
            else:
                return f"Failed to navigate to {url}: {error_msg}"
    
    async def click(self, page: Page, selector: str, timeout: int = 5000) -> str:
        """Click on an element."""
        try:
            # First wait for the element to be visible and enabled
            await page.wait_for_selector(selector, timeout=timeout, state="visible")
            
            # Check if element is clickable
            element = await page.query_selector(selector)
            if not element:
                return f"Element {selector} not found"
            
            # Scroll into view if needed
            await element.scroll_into_view_if_needed()
            
            # Perform the click
            await page.click(selector, timeout=timeout)
            return f"Successfully clicked element: {selector}"
        except Exception as e:
            error_msg = str(e)
            if "timeout" in error_msg.lower():
                return f"Timeout clicking element {selector}: element not clickable within {timeout}ms"
            elif "not visible" in error_msg.lower():
                return f"Failed to click element {selector}: element is not visible"
            elif "intercept" in error_msg.lower():
                return f"Failed to click element {selector}: element is intercepted by another element"
            else:
                return f"Failed to click element {selector}: {error_msg}"
    
    async def type_text(self, page: Page, selector: str, text: str, timeout: int = 5000) -> str:
        """Type text into an element."""
        try:
            # Wait for element and ensure it's enabled
            await page.wait_for_selector(selector, timeout=timeout, state="visible")
            
            # Clear existing text first
            await page.fill(selector, "", timeout=timeout)
            
            # Type the new text
            await page.fill(selector, text, timeout=timeout)
            
            return f"Successfully typed text into element: {selector}"
        except Exception as e:
            error_msg = str(e)
            if "timeout" in error_msg.lower():
                return f"Timeout typing into element {selector}: element not found or not enabled within {timeout}ms"
            elif "not editable" in error_msg.lower():
                return f"Failed to type into element {selector}: element is not editable"
            else:
                return f"Failed to type text into element {selector}: {error_msg}"
    
    async def screenshot(self, page: Page, path: Optional[str] = None, full_page: bool = False) -> str:
        """Take a screenshot of the page."""
        try:
            if path:
                # Ensure directory exists
                path_obj = Path(path)
                path_obj.parent.mkdir(parents=True, exist_ok=True)
                
                await page.screenshot(path=path, full_page=full_page)
                return f"Screenshot saved to: {path}"
            else:
                # Return base64 encoded screenshot with size limit
                screenshot_bytes = await page.screenshot(full_page=full_page)
                
                # Check size and warn if too large
                size_mb = len(screenshot_bytes) / (1024 * 1024)
                if size_mb > 5:  # Warn if screenshot is larger than 5MB
                    return f"Screenshot taken (size: {size_mb:.1f}MB - consider saving to file for large screenshots)"
                
                screenshot_b64 = base64.b64encode(screenshot_bytes).decode()
                return f"Screenshot taken (base64, size: {size_mb:.1f}MB): {screenshot_b64[:100]}..."
        except Exception as e:
            return f"Failed to take screenshot: {str(e)}"
    
    async def get_text(self, page: Page, selector: str, timeout: int = 5000) -> str:
        """Get text content from an element."""
        try:
            # First try to get a single element
            element = await page.wait_for_selector(selector, timeout=timeout)
            if element:
                text = await element.text_content()
                return text or ""
            return ""
        except Exception as e:
            # If single element fails, try to get multiple elements
            try:
                elements = await page.query_selector_all(selector)
                if elements:
                    texts = []
                    for element in elements:
                        text = await element.text_content()
                        if text:
                            texts.append(text.strip())
                    return " | ".join(texts) if texts else ""
                return f"Failed to get text from element {selector}: {str(e)}"
            except Exception:
                return f"Failed to get text from element {selector}: {str(e)}"
    
    async def wait_for_selector(self, page: Page, selector: str, timeout: int = 30000, state: str = "visible") -> str:
        """Wait for an element to appear."""
        valid_states = ["visible", "hidden", "attached", "detached"]
        if state not in valid_states:
            return f"Invalid state '{state}'. Must be one of: {', '.join(valid_states)}"
        
        try:
            await page.wait_for_selector(selector, timeout=timeout, state=state)
            return f"Element {selector} is now {state}"
        except Exception as e:
            error_msg = str(e)
            if "timeout" in error_msg.lower():
                return f"Timeout waiting for element {selector} to be {state} (waited {timeout}ms)"
            else:
                return f"Failed to wait for element {selector}: {error_msg}"
    
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
        valid_states = ["load", "domcontentloaded", "networkidle"]
        if state not in valid_states:
            return f"Invalid load state '{state}'. Must be one of: {', '.join(valid_states)}"
        
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
    
    async def fill_form(self, page: Page, form_data: dict[str, str], submit_selector: Optional[str] = None) -> str:
        """Fill multiple form fields and optionally submit the form."""
        results = []
        failed_fields = []
        
        for selector, value in form_data.items():
            try:
                await page.fill(selector, value, timeout=5000)
                results.append(f"✓ {selector}: filled")
            except Exception as e:
                failed_fields.append(f"✗ {selector}: {str(e)}")
        
        if submit_selector:
            try:
                await page.click(submit_selector, timeout=5000)
                results.append(f"✓ Form submitted via {submit_selector}")
            except Exception as e:
                results.append(f"✗ Failed to submit form: {str(e)}")
        
        summary = f"Filled {len(results) - len(failed_fields)}/{len(form_data)} fields"
        if failed_fields:
            summary += f" ({len(failed_fields)} failed)"
        
        return f"{summary}\n" + "\n".join(results + failed_fields)
    
    async def get_links(self, page: Page, limit: int = 50) -> str:
        """Get all links on the current page."""
        try:
            links = await page.evaluate(f"""
                () => {{
                    const links = Array.from(document.querySelectorAll('a[href]'));
                    return links.slice(0, {limit}).map(link => ({{
                        text: link.textContent.trim() || '[No text]',
                        href: link.href,
                        target: link.target || '_self'
                    }}));
                }}
            """)
            
            if not links:
                return "No links found on the page"
            
            result_lines = [f"Found {len(links)} links:"]
            for i, link in enumerate(links, 1):
                result_lines.append(f"{i}. {link['text']} -> {link['href']}")
            
            if len(links) == limit:
                result_lines.append(f"(Limited to first {limit} links)")
            
            return "\n".join(result_lines)
        except Exception as e:
            return f"Failed to get links: {str(e)}"
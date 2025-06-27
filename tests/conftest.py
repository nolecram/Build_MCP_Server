"""Test configuration and fixtures."""

import pytest
import asyncio
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from playwright_mcp_server.tools import PlaywrightTools


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def browser():
    """Create a browser instance for testing."""
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True)
    yield browser
    await browser.close()
    await playwright.stop()


@pytest.fixture
async def context(browser):
    """Create a browser context for testing."""
    context = await browser.new_context()
    yield context
    await context.close()


@pytest.fixture
async def page(context):
    """Create a page for testing."""
    page = await context.new_page()
    yield page
    await page.close()


@pytest.fixture
def tools():
    """Create a PlaywrightTools instance for testing."""
    return PlaywrightTools()
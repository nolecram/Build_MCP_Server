"""Tests for PlaywrightTools."""

import pytest
from playwright_mcp_server.tools import PlaywrightTools


class TestPlaywrightTools:
    """Test cases for PlaywrightTools."""
    
    @pytest.mark.asyncio
    async def test_navigate(self, page, tools):
        """Test navigation functionality."""
        result = await tools.navigate(page, "https://example.com")
        assert "Successfully navigated to: https://example.com" in result
        
        # Verify the page actually navigated
        url = await tools.get_url(page)
        assert "example.com" in url
    
    @pytest.mark.asyncio
    async def test_get_title(self, page, tools):
        """Test getting page title."""
        await tools.navigate(page, "https://example.com")
        title = await tools.get_title(page)
        assert isinstance(title, str)
        assert len(title) > 0
    
    @pytest.mark.asyncio
    async def test_get_url(self, page, tools):
        """Test getting page URL."""
        await tools.navigate(page, "https://example.com")
        url = await tools.get_url(page)
        assert "https://example.com" in url
    
    @pytest.mark.asyncio
    async def test_screenshot(self, page, tools):
        """Test taking a screenshot."""
        await tools.navigate(page, "https://example.com")
        result = await tools.screenshot(page)
        assert "Screenshot taken" in result
    
    @pytest.mark.asyncio
    async def test_evaluate_javascript(self, page, tools):
        """Test JavaScript evaluation."""
        await tools.navigate(page, "https://example.com")
        result = await tools.evaluate(page, "document.title")
        assert isinstance(result, str)
    
    @pytest.mark.asyncio
    async def test_wait_for_load_state(self, page, tools):
        """Test waiting for load state."""
        await tools.navigate(page, "https://example.com")
        result = await tools.wait_for_load_state(page, "load")
        assert "Page reached load state: load" in result
    
    @pytest.mark.asyncio
    async def test_get_text_from_body(self, page, tools):
        """Test getting text content."""
        await tools.navigate(page, "https://example.com")
        text = await tools.get_text(page, "body")
        assert isinstance(text, str)
        assert len(text) > 0
    
    @pytest.mark.asyncio
    async def test_click_nonexistent_element(self, page, tools):
        """Test clicking on a non-existent element."""
        await tools.navigate(page, "https://example.com")
        result = await tools.click(page, "#nonexistent-element", timeout=1000)
        assert "Failed to click element" in result
    
    @pytest.mark.asyncio
    async def test_type_into_nonexistent_element(self, page, tools):
        """Test typing into a non-existent element."""
        await tools.navigate(page, "https://example.com")
        result = await tools.type_text(page, "#nonexistent-input", "test text", timeout=1000)
        assert "Failed to type text" in result
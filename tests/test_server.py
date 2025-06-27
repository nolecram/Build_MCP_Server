"""Tests for the MCP Server."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from playwright_mcp_server.server import PlaywrightMCPServer


class TestPlaywrightMCPServer:
    """Test cases for PlaywrightMCPServer."""
    
    def test_server_initialization(self):
        """Test server initialization."""
        server = PlaywrightMCPServer()
        assert server.server is not None
        assert server.playwright is None
        assert server.browser is None
        assert server.context is None
        assert server.current_page is None
        assert server.pages == []
        assert server.tools is not None
    
    @pytest.mark.asyncio
    async def test_ensure_browser(self):
        """Test browser initialization."""
        server = PlaywrightMCPServer()
        
        # Mock the playwright objects
        with patch('playwright_mcp_server.server.async_playwright') as mock_playwright:
            mock_playwright_instance = AsyncMock()
            mock_playwright.return_value.start = AsyncMock(return_value=mock_playwright_instance)
            
            mock_browser = AsyncMock()
            mock_playwright_instance.chromium.launch = AsyncMock(return_value=mock_browser)
            
            mock_context = AsyncMock()
            mock_browser.new_context = AsyncMock(return_value=mock_context)
            
            mock_page = AsyncMock()
            mock_context.new_page = AsyncMock(return_value=mock_page)
            
            await server._ensure_browser()
            
            assert server.playwright == mock_playwright_instance
            assert server.browser == mock_browser
            assert server.context == mock_context
            assert server.current_page == mock_page
            assert len(server.pages) == 1
    
    @pytest.mark.asyncio
    async def test_new_tab(self):
        """Test creating a new tab."""
        server = PlaywrightMCPServer()
        
        # Mock browser setup
        with patch('playwright_mcp_server.server.async_playwright') as mock_playwright:
            mock_playwright_instance = AsyncMock()
            mock_playwright.return_value.start = AsyncMock(return_value=mock_playwright_instance)
            
            mock_browser = AsyncMock()
            mock_playwright_instance.chromium.launch = AsyncMock(return_value=mock_browser)
            
            mock_context = AsyncMock()
            mock_browser.new_context = AsyncMock(return_value=mock_context)
            
            mock_page1 = AsyncMock()
            mock_page2 = AsyncMock()
            mock_context.new_page = AsyncMock(side_effect=[mock_page1, mock_page2])
            
            # First ensure browser is set up
            await server._ensure_browser()
            
            # Now test new tab
            result = await server._new_tab()
            
            assert "New tab opened" in result
            assert len(server.pages) == 2
            assert server.current_page == mock_page2
    
    @pytest.mark.asyncio
    async def test_close_tab(self):
        """Test closing a tab."""
        server = PlaywrightMCPServer()
        
        # Mock browser setup with multiple tabs
        with patch('playwright_mcp_server.server.async_playwright') as mock_playwright:
            mock_playwright_instance = AsyncMock()
            mock_playwright.return_value.start = AsyncMock(return_value=mock_playwright_instance)
            
            mock_browser = AsyncMock()
            mock_playwright_instance.chromium.launch = AsyncMock(return_value=mock_browser)
            
            mock_context = AsyncMock()
            mock_browser.new_context = AsyncMock(return_value=mock_context)
            
            mock_page1 = AsyncMock()
            mock_page2 = AsyncMock()
            mock_context.new_page = AsyncMock(side_effect=[mock_page1, mock_page2])
            
            # Set up browser with two tabs
            await server._ensure_browser()
            await server._new_tab()
            
            # Close current tab
            result = await server._close_tab()
            
            assert "Tab closed" in result
            assert len(server.pages) == 1
            assert server.current_page == mock_page1
    
    @pytest.mark.asyncio
    async def test_close_last_tab(self):
        """Test that closing the last tab is prevented."""
        server = PlaywrightMCPServer()
        
        # Mock browser setup with one tab
        with patch('playwright_mcp_server.server.async_playwright') as mock_playwright:
            mock_playwright_instance = AsyncMock()
            mock_playwright.return_value.start = AsyncMock(return_value=mock_playwright_instance)
            
            mock_browser = AsyncMock()
            mock_playwright_instance.chromium.launch = AsyncMock(return_value=mock_browser)
            
            mock_context = AsyncMock()
            mock_browser.new_context = AsyncMock(return_value=mock_context)
            
            mock_page = AsyncMock()
            mock_context.new_page = AsyncMock(return_value=mock_page)
            
            await server._ensure_browser()
            
            # Try to close the only tab
            result = await server._close_tab()
            
            assert "Cannot close the last tab" in result
            assert len(server.pages) == 1
    
    @pytest.mark.asyncio
    async def test_cleanup(self):
        """Test cleanup functionality."""
        server = PlaywrightMCPServer()
        
        # Mock browser setup
        with patch('playwright_mcp_server.server.async_playwright') as mock_playwright:
            mock_playwright_instance = AsyncMock()
            mock_playwright.return_value.start = AsyncMock(return_value=mock_playwright_instance)
            
            mock_browser = AsyncMock()
            mock_playwright_instance.chromium.launch = AsyncMock(return_value=mock_browser)
            
            mock_context = AsyncMock()
            mock_browser.new_context = AsyncMock(return_value=mock_context)
            
            mock_page = AsyncMock()
            mock_context.new_page = AsyncMock(return_value=mock_page)
            
            await server._ensure_browser()
            
            # Test cleanup
            await server.cleanup()
            
            mock_page.close.assert_called_once()
            mock_context.close.assert_called_once()
            mock_browser.close.assert_called_once()
            mock_playwright_instance.stop.assert_called_once()
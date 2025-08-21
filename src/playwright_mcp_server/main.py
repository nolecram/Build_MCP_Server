"""Main entry point for the Playwright MCP Server."""

import asyncio
import logging
import signal
import sys
from typing import Optional

from playwright_mcp_server.server import PlaywrightMCPServer


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Main entry point wrapper for CLI."""
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


async def async_main() -> None:
    """Main entry point for the Playwright MCP Server."""
    server = PlaywrightMCPServer()
    
    # Set up signal handlers for graceful shutdown
    def signal_handler(signum, frame):
        logger.info(f"Received signal {signum}, shutting down...")
        raise KeyboardInterrupt()
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        logger.info("Starting Playwright MCP Server...")
        await server.run()
    except KeyboardInterrupt:
        logger.info("Shutting down server gracefully...")
    except Exception as e:
        logger.error(f"Error running server: {e}", exc_info=True)
        sys.exit(1)
    finally:
        try:
            await server.cleanup()
            logger.info("Server cleanup completed")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}", exc_info=True)


def cli_main() -> None:
    """CLI entry point wrapper."""
    main()


if __name__ == "__main__":
    main()
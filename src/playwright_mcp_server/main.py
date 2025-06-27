"""Main entry point for the Playwright MCP Server."""

import asyncio
import sys
from typing import Optional

from playwright_mcp_server.server import PlaywrightMCPServer


def main() -> None:
    """Main entry point wrapper for CLI."""
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)


async def async_main() -> None:
    """Main entry point for the Playwright MCP Server."""
    server = PlaywrightMCPServer()
    
    try:
        await server.run()
    except KeyboardInterrupt:
        print("\nShutting down server...")
    except Exception as e:
        print(f"Error running server: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        await server.cleanup()


def cli_main() -> None:
    """CLI entry point wrapper."""
    main()


if __name__ == "__main__":
    main()
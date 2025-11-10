#!/usr/bin/env python3
"""
IB Contact Discovery & Email Generator
Main entry point for contact discovery workflow.
"""

import sys
from src.discovery_cli import DiscoveryCLI


def main():
    """Run the contact discovery CLI."""
    try:
        cli = DiscoveryCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\n👋 Exiting... Good luck with your networking!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please report this issue if it persists.")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

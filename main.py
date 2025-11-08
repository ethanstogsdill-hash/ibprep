#!/usr/bin/env python3
"""
IB Networking Email Generator
Main entry point for the application.
"""

import sys
from src.cli import CLI


def main():
    """Run the email generator CLI."""
    try:
        cli = CLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\n👋 Exiting... Good luck with your networking!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please report this issue if it persists.")
        sys.exit(1)


if __name__ == "__main__":
    main()

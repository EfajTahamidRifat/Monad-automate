import asyncio
import importlib.util
import sys
import os
import random
from datetime import datetime, timedelta
from colorama import Fore, Style, init
from utils import data
from logger import logger

# Initialize colorama
init(autoreset=True)

# Configuration
SRC_FOLDER = "src"  # Folder containing the scripts
SCRIPTS = data["SCRIPTS"]  # Script names without .py extension
BORDER_WIDTH = 80
MIN_HOURS = 20
MAX_HOURS = 24
MIN_INTERVAL = 1  # Minimum minutes between different script executions
MAX_INTERVAL = 2  # Maximum minutes between different script executions


def print_border(message, color=Fore.WHITE):
    """[removed long docstring]"""Run all scripts in sequence with intervals, then wait for next cycle."""[removed long docstring]"""Main entry point."""
    # Ensure src directory exists
    if not os.path.isdir(SRC_FOLDER):
        logger.critical(f"Source folder '{SRC_FOLDER}' not found!")
        print(f"{Fore.RED}ERROR: Source folder '{SRC_FOLDER}' not found!{Style.RESET_ALL}")
        return

    print(f"{Fore.GREEN}Starting Multi-DEX Runner...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Looking for scripts in: {SRC_FOLDER}/{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Running scripts: {', '.join(SCRIPTS)}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Press Ctrl+C to stop the script{Style.RESET_ALL}")

    await schedule_scripts()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Script stopped by user{Style.RESET_ALL}")
    except Exception as e:
        logger.critical(f"Fatal error: {str(e)}")
        print(f"\n{Fore.RED}Fatal error: {str(e)}{Style.RESET_ALL}")
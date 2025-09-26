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
    """
    Print a colored border message.
    """
    border = f"{color}{'=' * BORDER_WIDTH}{Style.RESET_ALL}"
    print(border)
    print(f"{color}{message.center(BORDER_WIDTH)}{Style.RESET_ALL}")
    print(border)


async def schedule_scripts():
    """
    Run all scripts in sequence with random intervals,
    then wait for the next daily cycle.
    """
    while True:
        print_border("Starting Multi-DEX Runner", Fore.GREEN)

        for script_name in SCRIPTS:
            script_path = os.path.join(SRC_FOLDER, f"{script_name}.py")
            if not os.path.isfile(script_path):
                logger.error(f"Script not found: {script_name}.py")
                continue

            print_border(f"Running {script_name}", Fore.CYAN)
            try:
                spec = importlib.util.spec_from_file_location(script_name, script_path)
                module = importlib.util.module_from_spec(spec)
                sys.modules[script_name] = module
                spec.loader.exec_module(module)
                logger.info(f"{script_name} executed successfully.")
            except Exception as e:
                logger.error(f"Error running {script_name}: {e}")

            # Random interval between scripts
            delay = random.randint(MIN_INTERVAL, MAX_INTERVAL) * 60
            await asyncio.sleep(delay)

        # Wait for next cycle
        hours = random.randint(MIN_HOURS, MAX_HOURS)
        print_border(f"Cycle complete. Waiting {hours} hours for next run.", Fore.YELLOW)
        await asyncio.sleep(hours * 3600)


async def main():
    """
    Main entry point of the runner.
    Ensures src directory exists and starts scheduling.
    """
    if not os.path.isdir(SRC_FOLDER):
        logger.critical(f"Source folder '{SRC_FOLDER}' not found!")
        print(f"{Fore.RED}ERROR: Source folder '{SRC_FOLDER}' not found!{Style.RESET_ALL}")
        return

    print_border("Multi-DEX Runner Initialized", Fore.MAGENTA)
    await schedule_scripts()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Script stopped by user{Style.RESET_ALL}")
    except Exception as e:
        logger.critical(f"Fatal error: {str(e)}")
        print(f"\n{Fore.RED}Fatal error: {str(e)}{Style.RESET_ALL}")

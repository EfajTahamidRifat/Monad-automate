from src.stakers import MonadStaker
import logging
from utils import get_web3_connection, private_keys, data
from logger import color_print
import random
import asyncio
from web3.exceptions import Web3RPCError

# Constants
FUND_AMT = data["FUND_AMOUNT"]
FUNDER_PRIVATE_KEY = data["FUNDER_PRIVATE_KEY"]


class ZonaBet(MonadStaker):  # Inheriting attributes and method from MonadStaker
    def __init__(self, w3, private_key):
        """[removed long docstring]"""Place a bet on Zona Finance with the specified amount."""[removed long docstring]"""Place a single bet using the provided private key."""[removed long docstring]"""Run bets with multiple private keys from private_key.txt."""

    if not private_keys:
        logging.error("No private keys found in private_key.txt!")
        color_print("ERROR: No private keys found in private_key.txt!", "RED")
        return

    color_print(f"Starting Zona Bet with {len(private_keys)} accounts...", "GREEN")

    # Create tasks for each private key
    tasks = []
    for private_key in private_keys:
        tasks.append(place_bet(private_key))

    # Run all tasks concurrently
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    print("Starting Zona betting script...")
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("\nScript stopped by user")
    except Exception as e:
        logging.critical(f"Fatal error: {str(e)}")
        print(f"\nFatal error: {str(e)}")

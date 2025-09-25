import requests
from web3 import Web3
from typing import Dict, Any, Optional, List
import time
import asyncio
import random
from logger import logger as logging
from utils import timeout, color_print, get_web3_connection, get_phantom_headers, data, private_keys

# Constants
DAILY_SWAPS = data["DAILY_INTERACTION"]["DEX"]["monorail"]
FUND_AMT = data["FUND_AMOUNT"]
FUNDER_PRIVATE_KEY = data["FUNDER_PRIVATE_KEY"]


class MonorailSwapper:
    """[removed long docstring]"""
        Initialize the MonadSwapper with optional Web3 connection details.

        Args:
            private_key: Optional private key for signing transactions
        """[removed long docstring]"""
        Send native MON tokens to an address.

        Args:
            to_address: Recipient address
            amount: Amount in MON (will be converted to wei)
        """[removed long docstring]"""
        Get all token balances for a wallet address.

        Args:
            address: The wallet address to check balances for

        Returns:
            List of token balance objects
        """[removed long docstring]"""
        Display all token balances for a wallet address in a formatted way.
        MON is always displayed first with max 3 decimal places.

        Args:
            address: The wallet address to check balances for. If None, uses the address from the private key.
        """[removed long docstring]"""
        Get a swap quote from the Monorail pathfinder API.

        Args:
            amount: Amount of tokens to swap (in human-readable form)
            from_token: Token symbol to swap from (MON, WMON, CHOG, etc.)
            to_token: Token symbol to swap to
            sender_address: Address of the transaction sender
            slippage: Maximum acceptable slippage in percentage
            deadline: Transaction deadline in seconds
            source: Source identifier (default 'fe')

        Returns:
            Complete response from the pathfinder API
        """[removed long docstring]"""
        Build a swap transaction for the given token pair.

        Args:
            amount: Amount of tokens to swap (in human-readable form)
            from_token: Token symbol to swap from
            to_token: Token symbol to swap to
            sender_address: Address of the transaction sender

        Returns:
            Transaction object ready to be signed and sent
        """[removed long docstring]"""
        Execute a token swap with the given parameters. If transaction fails,
        retry up to 3 times with increased gas.

        Args:
            amount: Amount of tokens to swap (in human-readable form)
            from_token: Token symbol to swap from
            to_token: Token symbol to swap to

        Returns:
            Transaction hash of the executed swap

        Raises:
            ValueError: If private key is not set
            Exception: If all retry attempts fail
        """[removed long docstring]"""
        Calculate the price of one token in terms of another.

        Args:
            base_token: The token to get the price for (e.g., 'CHOG')
            quote_token: The token to express the price in (e.g., 'USDC')
            amount: The amount of base tokens to get quote for

        Returns:
            The price of base_token in terms of quote_token
        """[removed long docstring]"""
        Estimate the maximum output amount and route details for a swap.

        Args:
            from_token: Token to swap from
            to_token: Token to swap to
            input_amount: Amount of from_token to swap

        Returns:
            Dictionary with output amount, route details, and more
        """[removed long docstring]"""
        Get the address for a token symbol.

        Args:
            token: Token symbol (case-insensitive)

        Returns:
            Token address

        Raises:
            ValueError: If token is not recognized
        """[removed long docstring]"""Run swapper with multiple private keys from private_keys.txt."""

    if not private_keys:
        logging.error("No private keys found in private_keys.txt!")
        color_print("ERROR: No private keys found in private_keys.txt!", "RED")
        return

    color_print(f"Starting Project Swapper with {len(private_keys)} accounts...", "GREEN")

    # Create tasks for each private key
    tasks = []
    for private_key in private_keys:
        tasks.append(swap_tokens(private_key))

    # Run all tasks concurrently
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    print("Starting Project swapper script...")
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("\nScript stopped by user")
    except Exception as e:
        logging.critical(f"Fatal error: {str(e)}")
        print(f"\nFatal error: {str(e)}")

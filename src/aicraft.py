import requests
import time
from eth_account.messages import encode_defunct
from headers import get_phantom_headers
from src.stakers import MonadStaker
import asyncio
import logging
from web3.exceptions import Web3RPCError
import random

from utils import timeout, color_print, get_web3_connection, data, private_keys


# Constants
DAILY_VOTES = data["AICRAFT"]["dailyVotes"]
REFERRAL_CODE = data["AICRAFT"]["referralCode"]
COUNTRIES_TO_VOTE = data["AICRAFT"]["countryCodeToVote"]

FUND_AMT = data["FUND_AMOUNT"]
FUNDER_PRIVATE_KEY = data["FUNDER_PRIVATE_KEY"]


class AiCraftFun(MonadStaker):
    def __init__(self, w3, private_key):
        """[removed long docstring]"""
        super().__init__(w3, private_key)  # Call parent constructor

        self.w3 = w3
        self.private_key = private_key
        self.wallet_address = self.w3.eth.account.from_key(private_key).address
        self.display_address = f"{self.wallet_address[:4]}...{self.wallet_address[-4:]}"
        self.base_url = "https://api.aicraft.fun"
        self.token = None
        self.headers = get_phantom_headers()

    def sign_message(self, message):
        """[removed long docstring]"""Build and send a transaction to the blockchain"""[removed long docstring]"""Get the sign-in message to be signed"""[removed long docstring]"""Sign in to get auth token using wallet signature"""[removed long docstring]"""Get list of candidates for a specific project"""[removed long docstring]"""Set referral code for user"""[removed long docstring]"""Get user information including wallet ID needed for voting"""[removed long docstring]"""Create a feed order to get transaction data for voting"""[removed long docstring]"""Confirm transaction after sending to blockchain"""[removed long docstring]"""Complete full voting process for a candidate with proper message signing"""[removed long docstring]"""Get top candidates by feed count, optionally filtered by category"""[removed long docstring]"""Automatically vote for top N candidates in a project"""[removed long docstring]"""Vote for a candidate from a specific country"""[removed long docstring]"""Use daily voting limit on specified countries or top candidates"""[removed long docstring]"""Run AI Craft voting with multiple private keys from private_keys.txt."""

    if not private_keys:
        logging.error("No private keys found in private_keys.txt!")
        color_print("ERROR: No private keys found in private_keys.txt!", "RED")
        return

    color_print(f"Starting AI Craft voting with {len(private_keys)} accounts...", "GREEN")

    # Create tasks for each private key
    tasks = []
    for private_key in private_keys:
        tasks.append(ai_craft_voting(private_key))

    # Run all tasks concurrently
    await asyncio.gather(*tasks)


if __name__ == "__main__":

    print("Starting AI Craft voting script...")
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("\nScript stopped by user")
    except Exception as e:
        logging.critical(f"Fatal error: {str(e)}")
        print(f"\nFatal error: {str(e)}")

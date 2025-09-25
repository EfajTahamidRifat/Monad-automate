import asyncio
import random
from typing import Dict, List
from eth_account import Account
import aiohttp
from logger import logger
from colorama import init, Fore, Style
from utils import get_web3_connection, private_keys

# Initialize colorama
init(autoreset=True)

# Constants
RPC_URL = "https://testnet-rpc.project.xyz/"
EXPLORER_URL = "https://testnet.monadexplorer.com/tx/0x"
NFT_CONTRACT_ADDRESS = "0xb33D7138c53e516871977094B249C8f2ab89a4F4"
BORDER_WIDTH = 80
ATTEMPTS = 3
PAUSE_BETWEEN_ACTIONS = [5, 15]
MAX_AMOUNT_FOR_EACH_ACCOUNT = [1, 3]

# ERC1155 ABI
ERC1155_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "account", "type": "address"},
            {"internalType": "uint256", "name": "id", "type": "uint256"},
        ],
        "name": "balanceOf",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "quantity", "type": "uint256"}],
        "name": "mint",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "", "type": "address"}],
        "name": "mintedCount",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
]


def print_border(text: str, color=Fore.CYAN, width=BORDER_WIDTH):
    text = text.strip()
    if len(text) > width - 4:
        text = text[:width - 7] + "..."
    padded_text = f" {text} ".center(width - 2)
    print(f"{color}┌{'─' * (width - 2)}┐{Style.RESET_ALL}")
    print(f"{color}│{padded_text}│{Style.RESET_ALL}")
    print(f"{color}└{'─' * (width - 2)}┘{Style.RESET_ALL}")


def print_step(step: str, message: str):
    steps = {
        'balance': 'BALANCE',
        'mint': 'MINT NFT'
    }
    step_text = steps[step]
    formatted_step = f"{Fore.YELLOW}🔸 {Fore.CYAN}{step_text:<15}{Style.RESET_ALL}"
    print(f"{formatted_step} | {message}")


def print_completion_message(accounts: int, success_count: int):
    print(f"{Fore.GREEN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
    print_border("LILCHOGSTARS MINT - MONAD TESTNET", Fore.GREEN)
    print(f"{Fore.GREEN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}🎉 {'Completed NFT minting for ' + str(accounts) + ' accounts':^76}{Style.RESET_ALL}")
    completion_msg = f"ALL DONE - {accounts} ACCOUNTS"
    print_border(completion_msg, Fore.GREEN)
    success_msg = f"SUCCESSFUL NFT MINTS: {success_count}"
    print_border(success_msg, Fore.CYAN)
    print(f"{Fore.GREEN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")


class Lilchogstars:
    def __init__(self, account_index: int, private_key: str, session: aiohttp.ClientSession):
        self.account_index = account_index
        self.private_key = private_key
        self.session = session
        self.account = Account.from_key(private_key=private_key)
        self.web3 = get_web3_connection(use_async=True)
        self.nft_contract = self.web3.eth.contract(address=NFT_CONTRACT_ADDRESS, abi=ERC1155_ABI)

    async def get_nft_balance(self) -> int:
        """[removed long docstring]"""Mint Lilchogstars NFT."""[removed long docstring]"""Get gas parameters from the network."""[removed long docstring]"""Handle errors with random pause."""[removed long docstring]"""Run Lilchogstars script with multiple private keys from pvkey.txt."""

    if not private_keys:
        logger.error("No private keys found in pvkey.txt!")
        print_border("ERROR: No private keys found in pvkey.txt!", Fore.RED)
        return

    # Display initial title
    print(f"{Fore.GREEN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
    print_border("LILCHOGSTARS MINT - MONAD TESTNET", Fore.GREEN)
    print(f"{Fore.GREEN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}👥 {'Accounts'}: {len(private_keys):^76}{Style.RESET_ALL}")

    success_count = 0
    async with aiohttp.ClientSession() as session:
        for idx, private_key in enumerate(private_keys, start=1):
            wallet = Account.from_key(private_key).address
            wallet_short = f"{wallet[:5]}...{wallet[-5:]}"
            account_msg = f"ACCOUNT {idx}/{len(private_keys)} - {wallet_short}"
            print_border(account_msg, Fore.BLUE)
            lilchogstars = Lilchogstars(idx, private_key, session)
            logger.info(f"Processing account {idx}/{len(private_keys)}: {lilchogstars.account.address}")

            # Perform mint
            if await lilchogstars.mint():
                success_count += 1

            # Pause between accounts
            if idx < len(private_keys):
                pause = random.uniform(30, 60)
                pause_msg = f"Waiting {pause:.2f}s before next account..."
                print(f"{Fore.YELLOW}⏳ {pause_msg:^76}{Style.RESET_ALL}")
                await asyncio.sleep(pause)

    # Display completion message
    print_completion_message(accounts=len(private_keys), success_count=success_count)


if __name__ == "__main__":
    asyncio.run(run())

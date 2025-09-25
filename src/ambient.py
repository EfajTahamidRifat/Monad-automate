import asyncio
import random
from typing import Dict, List, Optional, Tuple
from eth_account import Account
from eth_abi import abi
from decimal import Decimal
from logger import logger
import aiohttp
from colorama import init, Fore, Style
from utils import get_web3_connection, private_keys, handle_funding_error


# Initialize colorama
init(autoreset=True)

# Constants
RPC_URL = "https://testnet-rpc.project.xyz/"
EXPLORER_URL = "https://testnet.monadexplorer.com/tx/0x"
AMBIENT_CONTRACT = "0x88B96aF200c8a9c35442C8AC6cd3D22695AaE4F0"
ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"
POOL_IDX = 36000
RESERVE_FLAGS = 0
TIP = 0
MAX_SQRT_PRICE = 21267430153580247136652501917186561137
MIN_SQRT_PRICE = 65537
BORDER_WIDTH = 80
ATTEMPTS = 3
PAUSE_BETWEEN_SWAPS = [30, 120]
PAUSE_BETWEEN_ACTIONS = [30, 300]

AMBIENT_TOKENS = {
    "usdt": {"address": "0x88b8E2161DEDC77EF4ab7585569D2415a1C1055D", "decimals": 6},
    "usdc": {"address": "0xf817257fed379853cDe0fa4F97AB987181B1E5Ea", "decimals": 6},
    "weth": {"address": "0xB5a30b0FDc5EA94A52fDc42e3E9760Cb8449Fb37", "decimals": 18},
    "wbtc": {"address": "0xcf5a6076cfa32686c0Df13aBaDa2b40dec133F1d", "decimals": 8},
    "seth": {"address": "0x836047a99e11F376522B447bffb6e3495Dd0637c", "decimals": 18},
}

ERC20_ABI = [
    {
        "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "spender", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
        ],
        "name": "approve",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "owner", "type": "address"},
            {"internalType": "address", "name": "spender", "type": "address"},
        ],
        "name": "allowance",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
]

AMBIENT_ABI = [
    {
        "inputs": [
            {"internalType": "uint16", "name": "callpath", "type": "uint16"},
            {"internalType": "bytes", "name": "cmd", "type": "bytes"},
        ],
        "name": "userCmd",
        "outputs": [{"internalType": "bytes", "name": "", "type": "bytes"}],
        "stateMutability": "payable",
        "type": "function",
    }
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
        'faucet': 'GET TOKENS',
        'approve': 'APPROVE',
        'swap': 'SWAP'
    }
    step_text = steps[step]
    formatted_step = f"{Fore.YELLOW}🔸 {Fore.CYAN}{step_text:<15}{Style.RESET_ALL}"
    print(f"{formatted_step} | {message}")


def print_completion_message(accounts: int, success_count: int):
    print(f"{Fore.GREEN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
    print_border("AMBIENT SWAP - MONAD TESTNET", Fore.GREEN)
    print(f"{Fore.GREEN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}🎉 Completed swap for {accounts} accounts{Style.RESET_ALL}")
    completion_msg = f"ALL DONE - {accounts} ACCOUNTS"
    print_border(completion_msg, Fore.GREEN)
    success_msg = f"SUCCESSFUL TRANSACTIONS: {success_count}"
    print_border(success_msg, Fore.CYAN)
    print(f"{Fore.GREEN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")


class AmbientDex:
    def __init__(self, account_index: int, private_key: str, session: aiohttp.ClientSession):
        self.account_index = account_index
        self.web3 = get_web3_connection(use_async=True)
        self.account = Account.from_key(private_key)
        self.session = session
        self.router_contract = self.web3.eth.contract(address=AMBIENT_CONTRACT, abi=AMBIENT_ABI)

    async def get_gas_params(self) -> Dict[str, int]:
        """[removed long docstring]"""Convert amount to wei based on token decimals."""[removed long docstring]"""Convert from wei to token units."""[removed long docstring]"""Get list of tokens with balance greater than 0."""[removed long docstring]"""Tạo dữ liệu giao dịch swap cho Ambient DEX."""[removed long docstring]"""Thực hiện giao dịch và chờ xác nhận."""[removed long docstring]"""Phê duyệt token cho Ambient DEX."""[removed long docstring]"""Perform a swap on Ambient DEX."""[removed long docstring]"""Xử lý lỗi với pause ngẫu nhiên."""[removed long docstring]"""Run Ambient script with multiple private keys from pvkey.txt."""

    if not private_keys:
        logger.error("No private keys found in pvkey.txt!")
        print_border("ERROR: No private keys found in pvkey.txt!", Fore.RED)
        return

    # Display title
    print(f"{Fore.GREEN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
    print_border("AMBIENT SWAP - MONAD TESTNET", Fore.GREEN)
    print(f"{Fore.GREEN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}👥 Accounts: {len(private_keys):^76}{Style.RESET_ALL}")

    success_count = 0
    async with aiohttp.ClientSession() as session:
        try:  # Add try block
            for idx, private_key in enumerate(private_keys, start=1):
                wallet = Account.from_key(private_key).address
                wallet_short = f"{wallet[:5]}...{wallet[-5:]}"
                account_msg = f"ACCOUNT {idx}/{len(private_keys)} - {wallet_short}"
                print_border(account_msg, Fore.BLUE)
                ambient = AmbientDex(idx, private_key, session)
                logger.info(f"Processing account {idx}/{len(private_keys)}: {ambient.account.address}")

                # Execute swap
                try:
                    tx_hash = await ambient.swap(percentage_to_swap=100.0, swap_type="regular")
                    if tx_hash:
                        success_count += 1
                except Exception as e:
                    logger.error(f"[{idx}] Failed to execute swap: {str(e)}")
                    print_step('swap', f"{Fore.RED}✘ Swap failed: {str(e)}{Style.RESET_ALL}")

                # Pause between accounts
                if idx < len(private_keys):
                    pause = random.uniform(10, 30)
                    pause_msg = f"Waiting {pause:.2f}s before next account..."
                    print(f"{Fore.YELLOW}⏳ {pause_msg:^76}{Style.RESET_ALL}")
                    await asyncio.sleep(pause)

        finally:  # Ensure session is properly closed
            pass  # Session will be closed by async with context manager

    # Display completion message
    print_completion_message(accounts=len(private_keys), success_count=success_count)

if __name__ == "__main__":
    asyncio.run(run())

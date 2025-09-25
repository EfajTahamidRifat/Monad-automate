"""[removed long docstring]"""
        Initialize a MonadStaker with your private key

        Args:
            private_key (str): Private key of the wallet to stake from
        """[removed long docstring]"""
        Stake MON tokens to receive sMON tokens through Kintsu

        Args:
            amount_to_stake (float): Amount of MON to stake in ether units

        Returns:
            str: Transaction hash if successful, None otherwise
        """[removed long docstring]"""
        Stake MON tokens to receive aprMON tokens through Apriori

        Args:
            amount_to_stake (float): Amount of MON to stake in ether units

        Returns:
            str: Transaction hash if successful, None otherwise
        """[removed long docstring]"""Helper method to sign and send a transaction"""[removed long docstring]"""Run staker with multiple private keys from private_keys.txt."""

    if not private_keys:
        logging.error("No private keys found in private_keys.txt!")
        color_print("ERROR: No private keys found in private_keys.txt!", "RED")
        return

    color_print(f"Starting Project Staker with {len(private_keys)} accounts...", "GREEN")

    # Create tasks for each private key
    tasks = []
    for private_key in private_keys:
        tasks.append(stake_token(private_key))

    # Run all tasks concurrently
    await asyncio.gather(*tasks)


if __name__ == "__main__":

    print("Starting Project staker script...")
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("\nScript stopped by user")
    except Exception as e:
        logging.critical(f"Fatal error: {str(e)}")
        print(f"\nFatal error: {str(e)}")
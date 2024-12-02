import csv

from loguru import logger

from data import config
from data.models import Settings, WalletCSV
from eth_async.client import Client
from eth_async.models import Networks
from utils.db_api.models import Wallet
from utils.db_api.wallet_api import get_wallet, db


class Import:
    @staticmethod
    def get_wallets_from_csv(csv_path: str, skip_first_line: bool = True) -> list[WalletCSV]:
        wallets = []

        with open(csv_path) as f:
            reader = csv.reader(f)
            for row in reader:
                if skip_first_line:
                    skip_first_line = False
                    continue
                wallets.append(WalletCSV(
                    private_key=row[0],
                    sol_private_key=row[1],
                    proxy=row[2],
                    name=row[3]
                ))
        return wallets

    @staticmethod
    async def wallets():
        wallets = Import.get_wallets_from_csv(csv_path=config.IMPORT_FILE)

        imported = []
        edited = []
        total = len(wallets)

        for wallet in wallets:
            wallet_instance = get_wallet(private_key=wallet.private_key)
            if wallet_instance and (
                    wallet_instance.proxy != wallet.proxy or
                    wallet_instance.name != wallet.name
            ):
                wallet_instance.proxy = wallet.proxy
                wallet_instance.name = wallet.name
                db.commit()
                edited.append(wallet_instance)

            if not wallet_instance:
                client = Client(private_key=wallet.private_key, network=Networks.NEON)
                wallet_instance = Wallet(
                    private_key=wallet.private_key,
                    sol_private_key=wallet.sol_private_key,
                    address=client.account.address,
                    proxy=wallet.proxy,
                    name=wallet.name,
                )
                db.insert(wallet_instance)
                imported.append(wallet_instance)

        logger.success(f'Done! imported wallets: {len(imported)}/{total}; '
                       f'edited wallets: {len(edited)}/{total}; total: {total}')
import asyncio
import random
from datetime import datetime

from data.config import DELAY_IN_CASE_OF_ERROR
from data.models import Settings
from eth_async.client import Client
from eth_async.models import Networks
from functions.select_random_action import select_random_action
from tasks.controller import Controller
from utils.db_api.models import Wallet
from utils.db_api.wallet_api import db, get_next_action_time
from utils.update_expired import update_expired, update_next_action_time
from functions.notificator import Notificator


async def starter():
    settings = Settings()
    delay = 10

    update_expired()
    await asyncio.sleep(5)

    next_action_time = get_next_action_time()
    Notificator.info(text=f'The next closest action will be performed at {next_action_time}')

    while True:
        try:
            now = datetime.now()

            wallet: Wallet = db.one(
                Wallet, Wallet.next_action_time <= now,
            )

            if not wallet:
                await asyncio.sleep(delay)
                continue

            client = Client(private_key=wallet.private_key, network=Networks.NEON, proxy=wallet.proxy)
            controller = Controller(client=client)
            action = await select_random_action(controller=controller, wallet=wallet)

            if not action:
                Notificator.error(f'{wallet.name} | select_random_action | can not choose the action')
                update_next_action_time(private_key=wallet.private_key, seconds=DELAY_IN_CASE_OF_ERROR)
                continue

            if action == 'Insufficient balance':
                Notificator.error(f'{wallet.name}: Insufficient balance')
                update_next_action_time(private_key=wallet.private_key, seconds=DELAY_IN_CASE_OF_ERROR)
                continue

            status = await action()

            if 'Failed' not in status:
                update_next_action_time(
                    private_key=wallet.private_key,
                    seconds=random.randint(settings.actions_delay.from_, settings.actions_delay.to_)
                )
                Notificator.success(f'{wallet.name}: {status}')

                next_action_time = get_next_action_time()
                Notificator.info(f'The next closest action will be performed at {next_action_time}')

                await asyncio.sleep(delay)

            else:
                update_next_action_time(private_key=wallet.private_key, seconds=DELAY_IN_CASE_OF_ERROR)
                db.commit()
                Notificator.error(f'{wallet.name}: {status}')


        except BaseException as e:
            Notificator.exception(f'Something went wrong: {e}')
            await asyncio.sleep(500)

        finally:
            await asyncio.sleep(delay)



if __name__ == '__main__':
    asyncio.run(starter())

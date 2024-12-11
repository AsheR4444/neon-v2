import random
from datetime import datetime, timedelta

from loguru import logger
from sqlalchemy import select

from data.models import Settings
from utils.db_api.wallet_api import db, get_wallet
from utils.db_api.models import Wallet


def update_expired() -> None:
    now = datetime.now()
    stmt = select(Wallet).where(
        Wallet.next_action_time.is_(None),
    )

    expired_wallets: list[Wallet] = db.all(stmt=stmt)

    if not expired_wallets:
        return

    settings = Settings()
    for wallet in expired_wallets:
        wallet.next_action_time = now + timedelta(
            seconds=random.randint(0, int(settings.actions_delay.to_ / 2))
        )
        logger.info(
            f'{wallet.name}: Action time was re-generated: '
            f'{wallet.next_action_time}.'
        )

    db.commit()

def update_next_action_time(private_key: str, seconds: int) -> bool:
    try:
        now = datetime.now()
        wallet = get_wallet(private_key=private_key)
        wallet.next_action_time = now + timedelta(seconds=seconds)
        db.commit()

        return True
    except BaseException:
        return False
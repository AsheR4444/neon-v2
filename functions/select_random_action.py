import random

from data.models import Settings, Contracts
from tasks.controller import Controller
from utils.db_api.models import Wallet


async def select_random_action(controller: Controller, wallet: Wallet):
    settings = Settings()

    possible_actions = []
    weights = []

    neon_balance = await controller.client.wallet.balance()

    # if float(neon_balance.Ether) < settings.minimal_balance:
    #     if settings.use_neonpass_bridge:
    #         # TODO: тут нужно возвращать функцию bridge_to_neon а не вызывать её
    #         # TODO: нужно передать wallet с типом из бд
    #         await bridge_to_neon(wallet=wallet)
    #         return
    #     return 'Insufficient balance'

    sufficient_balance = float(neon_balance.Ether) > settings.minimal_balance

    if not sufficient_balance:
        return 'Insufficient balance'

    usdc_balance = await controller.client.wallet.balance(token=Contracts.NEON_USDC)
    usdt_balance = await controller.client.wallet.balance(token=Contracts.NEON_USDT)
    wsol_balance = await controller.client.wallet.balance(token=Contracts.WSOL)

    if usdt_balance.Wei:
        possible_actions += [
            controller.neon.swap_usdt_to_wneon,
            controller.neon.swap_usdt_to_wsol,
            controller.neon.swap_usdt_to_usdc,
        ]
        weights += [
            1,
            1,
            1,
        ]

    if usdc_balance.Wei:
        possible_actions += [
            controller.neon.swap_usdc_to_wneon,
            controller.neon.swap_usdc_to_wsol,
            controller.neon.swap_usdc_to_usdt,
        ]
        weights += [
            1,
            1,
            1,
        ]

    if wsol_balance.Wei:
        possible_actions += [
            controller.neon.swap_wsol_to_wneon,
            controller.neon.swap_wsol_to_usdc,
            controller.neon.swap_wsol_to_usdt,
        ]
        weights += [
            1,
            1,
            1,
        ]

    if sufficient_balance:
        possible_actions += [
            controller.neon.swap_wneon_to_usdt,
            controller.neon.swap_wneon_to_usdc,
            controller.neon.swap_wneon_to_wsol,
        ]
        weights += [
            1,
            1,
            1,
        ]

    if possible_actions:
        action = None
        while not action:
            action = random.choices(possible_actions, weights=weights)[0]
        else:
            return action
    return None
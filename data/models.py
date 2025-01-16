from dataclasses import dataclass

from eth_async.models import RawContract, DefaultABIs
from eth_async.utils.files import read_json
from eth_async.classes import Singleton, AutoRepr

from data.config import ABIS_DIR, SETTINGS_FILE


@dataclass
class FromTo:
    from_: int | float
    to_: int | float

class Settings(Singleton, AutoRepr):
    def __init__(self):
        json_data = read_json(path=SETTINGS_FILE)

        self.maximum_gas_price: int = json_data['maximum_gas_price']
        self.minimal_balance: float = json_data['minimal_balance']
        self.eth_amount_for_swap: FromTo = FromTo(from_=json_data['eth_amount_for_swap']['from'], to_=json_data['eth_amount_for_swap']['to'])
        self.actions_delay: FromTo = FromTo(
            from_=json_data['actions_delay']['from'], to_=json_data['actions_delay']['to']
        )
        self.telegram_notifications_enabled: bool = json_data['telegram']['send_notifications']
        self.telegram_bot_key: str = json_data['telegram']['bot_key']
        self.telegram_chat_id: str = json_data['telegram']['chat_id']
        # self.use_neonpass_bridge: bool = json_data['use_neonpass_bridge']
        # self.use_swap_on_jupiter: bool = json_data['swap_on_jupiter']['enabled']
        # self.swap_on_jupiter_amount: FromTo = FromTo(from_=json_data['swap_on_jupiter']['amount']['from'], to_=json_data['swap_on_jupiter']['amount']['to'])


@dataclass
class WalletCSV:
    header = ['private_key','sol_private_key','proxy','name']

    def __init__(self, private_key: str, sol_private_key:str, proxy: str = '', name: str = ''):
        self.private_key = private_key
        self.sol_private_key = sol_private_key
        self.proxy = proxy
        self.name = name

class Contracts(Singleton):
    Neon = RawContract(
        title='Neon',
        address='0xc0E49f8C615d3d4c245970F6Dc528E4A47d69a44',
        abi=DefaultABIs.Token
    )

    MORA_NEON = RawContract(
        title='Mora',
        address='0x594e37B9F39f5D31DEc4a8c1cC4fe2E254153034',
        abi=read_json(path=(ABIS_DIR, 'mora.json'))
    )

    NEON_USDT = RawContract(
        title='USDT',
        address='0x5f0155d08eF4aaE2B500AefB64A3419dA8bB611a',
        abi=DefaultABIs.Token
    )

    WNEON = RawContract(
        title='Wrapped Neon',
        address='0x202C35e517Fa803B537565c40F0a6965D7204609',
        abi=read_json(path=(ABIS_DIR, 'WETH.json'))
    )

    WSOL = RawContract(
        title='Wrapped Sol',
        address='0x5f38248f339Bf4e84A2caf4e4c0552862dC9F82a',
        abi=DefaultABIs.Token
    )

    NEON_USDC = RawContract(
        title='USDC',
        address='0xEA6B04272f9f62F997F666F07D3a974134f7FFb9',
        abi=DefaultABIs.Token
    )

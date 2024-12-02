import asyncio

import aiohttp

from data.models import Settings
from eth_async.client import Client
from eth_async.models import TokenAmount, RawContract
from eth_async.utils.utils import randfloat


class Base:
    def __init__(self, client: Client):
        self.client = client

    @staticmethod
    async def get_token_price(token: str) -> float | None:
        for _ in range(5):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                            f'https://api.neonscan.org/token/overview?address={token}') as r:
                        if r.status != 200:
                            return None
                        result_dict = await r.json()
                        if 'data' not in result_dict:
                            return None
                        return float(result_dict['data']['price'])
            except Exception as e:
                await asyncio.sleep(5)
        raise ValueError(f'Can not get price from Neon')

    async def approve_interface(self, token_address, spender, amount: TokenAmount | None = None) -> bool:
        balance = await self.client.wallet.balance(token=token_address)
        if balance.Wei <= 0:
            return False

        if not amount or amount.Wei > balance.Wei:
            amount = balance

        approved = await self.client.transactions.approved_amount(
            token=token_address,
            spender=spender,
            owner=self.client.account.address
        )

        if amount.Wei <= approved.Wei:
            return True

        tx = await self.client.transactions.approve(
            token=token_address,
            spender=spender,
            amount=amount
        )

        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
        if receipt:
            return True

        return False

    async def get_token_info(self, contract_address):
        contract = await self.client.contracts.default_token(contract_address=contract_address)
        print('name:', await contract.functions.name().call())
        print('symbol:', await contract.functions.symbol().call())
        print('decimals:', await contract.functions.decimals().call())

    @staticmethod
    def parse_params(params: str, has_function: bool = True):
        if has_function:
            function_signature = params[:10]
            print('function_signature', function_signature)
            params = params[10:]
        while params:
            print(params[:64])
            params = params[64:]

    @staticmethod
    def get_eth_amount_for_swap():
        settings = Settings()
        return TokenAmount(
            amount=randfloat(
                from_=settings.eth_amount_for_swap.from_,
                to_=settings.eth_amount_for_swap.to_,
                step=0.0000001
            )
        )

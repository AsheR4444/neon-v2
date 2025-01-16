import asyncio
import time
import random
from loguru import logger

from web3 import Web3

from web3.types import TxParams
from data.models import Contracts
from eth_async.models import TokenAmount, TxArgs
from functions.notificator import Notificator
from tasks.base import Base


class Mora(Base):
    """
        FROM NEON
    """
    PATH_FROM_WNEON_TO_USDT = [
        Contracts.WNEON.address,
        Contracts.NEON_USDT.address
    ]
    PATH_FROM_WNEON_TO_USDC = [
        Contracts.WNEON.address,
        Contracts.NEON_USDC.address
    ]
    PATH_FROM_WNEON_TO_WSOL = [
        Contracts.WNEON.address,
        Contracts.WSOL.address
    ]
    """
        TO NEON
    """
    PATH_FROM_USDT_TO_WNEON = [
        Contracts.NEON_USDT.address,
        Contracts.WNEON.address
    ]
    PATH_FROM_USDC_TO_WNEON = [
        Contracts.NEON_USDC.address,
        Contracts.WNEON.address
    ]
    PATH_FROM_WSOL_TO_WNEON = [
        Contracts.WSOL.address,
        Contracts.WNEON.address
    ]
    """
        TOKEN TO TOKEN
    """
    PATH_FROM_USDC_TO_USDT = [
        Contracts.NEON_USDC.address,
        Contracts.NEON_USDT.address,
    ]
    PATH_FROM_USDT_TO_USDC = [
        Contracts.NEON_USDT.address,
        Contracts.NEON_USDC.address,
    ]
    PATH_FROM_USDT_TO_WSOL = [
        Contracts.NEON_USDT.address,
        Contracts.WSOL.address,
    ]
    PATH_FROM_USDC_TO_WSOL = [
        Contracts.NEON_USDC.address,
        Contracts.WSOL.address,
    ]
    PATH_FROM_WSOL_TO_USDC = [
        Contracts.WSOL.address,
        Contracts.NEON_USDC.address,
    ]
    PATH_FROM_WSOL_TO_USDT = [
        Contracts.WSOL.address,
        Contracts.NEON_USDT.address,
    ]

    async def _swap(self, path: list[bytes], amount: TokenAmount | None = None) -> str:
        slippage = 8

        to_token_address = Web3.to_checksum_address(path[-1])
        to_token = await self.client.contracts.default_token(contract_address=to_token_address)
        to_token_name = await to_token.functions.symbol().call()

        from_token_address = Web3.to_checksum_address(path[0])
        from_token = await self.client.contracts.default_token(contract_address=from_token_address)
        from_token_name = await from_token.functions.symbol().call()
        from_token_price = await Mora.get_token_price(token=from_token_address)

        from_token_is_neon = from_token_address.upper() == Contracts.WNEON.address.upper()
        to_token_is_neon = from_token_address.upper() == Contracts.WNEON.address.upper()
        to_token_price = await Mora.get_token_price(token=to_token_address)
        is_token_to_token = not from_token_is_neon and not to_token_is_neon

        failed_text = f'Failed swap {from_token_name} to {to_token_name} via Mora'
        logger.info(f'Start to swap {from_token_name} to {to_token_name} via Mora')

        if not amount:
            amount = await self.client.wallet.balance(token=from_token.address)

        contract = await self.client.contracts.get(contract_address=Contracts.MORA_NEON)

        if not from_token_is_neon:
            if await self.approve_interface(
                    token_address=from_token.address,
                    spender=contract.address,
                    amount=TokenAmount(amount=amount.Wei, decimals=6)
            ):
                await asyncio.sleep(random.randint(5, 10))
            else:
                return f"{failed_text} | can't approve"

        amount_out_min = hex(TokenAmount(
            amount=float(amount.Ether) * from_token_price / to_token_price * (100 - slippage) / 100,
            decimals=await self.client.transactions.get_decimals(contract=to_token_address)
        ).Wei)


        if from_token_is_neon:
            args = TxArgs(
                amountOutMin=int(amount_out_min, 16),
                path=path,
                address=self.client.account.address,
                deadline=int(time.time() + 60)
            )
        else:
            args = TxArgs(
                amountIn=amount.Wei,
                amountOutMin=int(amount_out_min, 16),
                path=path,
                address=self.client.account.address,
                deadline=int(time.time() + 60)
            )

        function_name = (
            'swapExactTokensForTokens' if is_token_to_token else
            'swapExactETHForTokens' if from_token_is_neon else
            'swapExactTokensForETH'
        )

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI(function_name, args=args.tuple()),
            value=amount.Wei if from_token_is_neon \
            else 0
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=200)

        if receipt and 'status' in receipt and receipt['status'] == 1:
            return f'{amount.Ether} {from_token_name} was swapped to {to_token_name} via Mora: https://neonscan.org/tx/{tx.hash.hex()}'

        return f'{failed_text} https://neonscan.org/tx/{tx.hash.hex()}'

    '''
        FROM NEON
    '''
    async def swap_wneon_to_usdt(self):
        amount = Base.get_eth_amount_for_swap()
        print(amount)
        return await self._swap(path=Mora.PATH_FROM_WNEON_TO_USDT, amount=amount)

    async def swap_wneon_to_usdc(self):
        amount = Base.get_eth_amount_for_swap()
        return await self._swap(path=Mora.PATH_FROM_WNEON_TO_USDC, amount=amount)

    async def swap_wneon_to_wsol(self):
        amount = Base.get_eth_amount_for_swap()
        return await self._swap(path=Mora.PATH_FROM_WNEON_TO_WSOL, amount=amount)
    '''
        TO NEON
    '''
    async def swap_usdt_to_wneon(self):
        return await self._swap(path=Mora.PATH_FROM_USDT_TO_WNEON)

    async def swap_wsol_to_wneon(self):
        return await self._swap(path=Mora.PATH_FROM_USDT_TO_WNEON)

    async def swap_usdc_to_wneon(self):
        return await self._swap(path=Mora.PATH_FROM_USDC_TO_WNEON)
    '''
        TOKEN TO TOKEN
    '''
    async def swap_usdc_to_usdt(self):
        return await self._swap(path=Mora.PATH_FROM_USDC_TO_USDT)

    async def swap_usdt_to_usdc(self):
        return await self._swap(path=Mora.PATH_FROM_USDT_TO_USDC)

    async def swap_usdt_to_wsol(self):
        return await self._swap(path=Mora.PATH_FROM_USDT_TO_WSOL)

    async def swap_usdc_to_wsol(self):
        return await self._swap(path=Mora.PATH_FROM_USDC_TO_WSOL)

    async def swap_wsol_to_usdc(self):
        return await self._swap(path=Mora.PATH_FROM_WSOL_TO_USDC)

    async def swap_wsol_to_usdt(self):
        return await self._swap(path=Mora.PATH_FROM_WSOL_TO_USDT)

    async def unwrap_neon(self):
        amount = await self.client.wallet.balance(token=Contracts.WNEON)

        contract = await self.client.contracts.get(contract_address=Contracts.WNEON)

        args = TxArgs(wad=amount.Wei)

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI("withdraw", args=args.tuple()),
            value=0
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=200)

        if receipt and 'status' in receipt and receipt['status'] == 1:
            return f'{amount.Ether} WNEON was swapped to NEON via Mora: https://neonscan.org/tx/{tx.hash.hex()}'

        return f'fail https://neonscan.org/tx/{tx.hash.hex()}'
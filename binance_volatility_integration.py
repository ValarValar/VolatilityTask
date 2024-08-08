import asyncio
import logging
from typing import Optional, Tuple
from decimal import Decimal

from VolatilityTask.base_volatility_integration import BaseIntegrationClient, StockMarketIntegration
from VolatilityTask.consts import BINANCE_INTERVAL_MAPPING, BASE_INTERVAL_HOUR
from VolatilityTask.metrics_math import calculate_volatility
from VolatilityTask.serializers import IntegrationVolatilityMetric

logger = logging.getLogger("asyncio")


class BinanceIntegrationClient(BaseIntegrationClient):
    name = 'Binance Client'
    stock_base_url: str = 'https://api.binance.com/api/v3/klines'
    interval_mapping = BINANCE_INTERVAL_MAPPING

    async def _prepare_params(self, **kwargs) -> dict:
        interval: Optional[str] = kwargs.get('interval')
        symbol_pair: Optional[str] = kwargs.get('symbol_pair')
        interval = self._map_interval(interval)

        if not interval or not symbol_pair:
            logger.error(f'Provided to {self.name} invalid params')
            return {}
        return {'symbol': symbol_pair, 'interval': interval}


class BinanceStockMarketIntegration(StockMarketIntegration):
    high_price_index: int = 2
    low_price_index: int = 3

    def __init__(self, symbol_pairs: Tuple[str, ...]):
        self.client: Optional[BinanceIntegrationClient] = None
        self.symbol_pairs = symbol_pairs

    async def _get_client(self) -> BinanceIntegrationClient:
        if not self.client:
            return BinanceIntegrationClient()
        return self.client

    async def _get_symbol_pair_data_for_interval(self, symbol_pair: str, interval: str) -> list[list]:
        client = await self._get_client()
        return await client.get_pair_data(symbol_pair=symbol_pair, interval=interval)

    async def _calculate_pair_volatility_for_interval(
            self, symbol_pair: str, interval: str
    ) -> IntegrationVolatilityMetric:
        pair_datas = await self._get_symbol_pair_data_for_interval(symbol_pair, interval)
        if not pair_datas:
            return IntegrationVolatilityMetric(symbol_pair, Decimal(0))

        max_high_price = Decimal(pair_datas[0][self.high_price_index])
        min_low_price = Decimal(pair_datas[0][self.low_price_index])

        for pair_data in pair_datas:
            max_high_price = max(max_high_price, Decimal(pair_data[self.high_price_index]))
            min_low_price = min(min_low_price, Decimal(pair_data[self.low_price_index]))
        volatility = await calculate_volatility(max_high_price, min_low_price)
        return IntegrationVolatilityMetric(symbol_pair, volatility)

    async def calculate_all_symbols_metrics_for_interval(
            self, interval: str
    ) -> Tuple[IntegrationVolatilityMetric, ...]:
        tasks = []
        for symbol_pair in self.symbol_pairs:
            task = asyncio.create_task(
                self._calculate_pair_volatility_for_interval(symbol_pair=symbol_pair, interval=interval)
            )
            tasks.append(task)
        symbol_pair_volatilities = await asyncio.gather(*tasks, return_exceptions=True)
        return symbol_pair_volatilities

    async def calculate_all_symbols_metrics_for_last_hour(self) -> Tuple[IntegrationVolatilityMetric, ...]:
        return await self.calculate_all_symbols_metrics_for_interval(BASE_INTERVAL_HOUR)

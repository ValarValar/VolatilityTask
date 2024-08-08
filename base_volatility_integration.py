import logging
from abc import ABC, abstractmethod
from typing import Optional, Tuple

from VolatilityTask.serializers import IntegrationVolatilityMetric

logger = logging.getLogger("asyncio")


class BaseIntegrationClient(ABC):
    @property
    @abstractmethod
    def stock_base_url(self) -> str:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def interval_mapping(self) -> dict:
        pass

    @abstractmethod
    async def _prepare_params(self, **kwargs) -> dict:
        pass

    def _map_interval(self, interval: Optional[str]) -> Optional[str]:
        if not interval:
            return None
        return self.interval_mapping.get(interval)


class StockMarketIntegration(ABC):
    @property
    @abstractmethod
    def high_price_index(self) -> int:
        pass

    @property
    @abstractmethod
    def low_price_index(self) -> int:
        pass

    @abstractmethod
    async def _get_client(self) -> BaseIntegrationClient:
        pass

    @abstractmethod
    async def _calculate_pair_volatility_for_interval(self, symbol_pair: str, interval: str):
        pass

    @abstractmethod
    async def calculate_all_symbols_metrics_for_interval(
            self, interval: str
    ) -> Tuple[IntegrationVolatilityMetric, ...]:
        pass

    @abstractmethod
    async def calculate_all_symbols_metrics_for_last_hour(self) -> Tuple[IntegrationVolatilityMetric, ...]:
        pass

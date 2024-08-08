import asyncio
import time

from VolatilityTask.integration.base_integration import BaseStockMarketIntegration
from VolatilityTask.integration.binance_integration import BinanceBaseStockMarketIntegration
from VolatilityTask.consts import SYMBOL_PAIRS


async def collect_metrics(integration: BaseStockMarketIntegration):
    result = await asyncio.create_task(integration.calculate_all_symbols_metrics_for_last_hour())
    for pair_metrics in result:
        print(pair_metrics)


start_time = time.time()

asyncio.run(collect_metrics(BinanceBaseStockMarketIntegration(SYMBOL_PAIRS)))

print((time.time() - start_time))

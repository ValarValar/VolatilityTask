import asyncio
import time

from VolatilityTask.base_volatility_integration import StockMarketIntegration
from VolatilityTask.binance_volatility_integration import BinanceStockMarketIntegration
from VolatilityTask.consts import SYMBOL_PAIRS


async def collect_metrics(integration: StockMarketIntegration):
    result = await asyncio.create_task(integration.calculate_all_symbols_metrics_for_last_hour())
    for pair_metrics in result:
        print(pair_metrics)


start_time = time.time()

asyncio.run(collect_metrics(BinanceStockMarketIntegration(SYMBOL_PAIRS)))

print((time.time() - start_time))

# VolatilityTask
## Task Specification
Calculate volatility for last 1 hour for few symbols:

* BTCUSDT
* ETHBTC
* LTCBTC
* ABOBABTC
* DGBBTC
* DOGEBTC

Formula:
__volatility = (max_high - min_low) / min_low * 100__

### Data source:
https://api.binance.com/api/v3/klines
### Docs for method:
https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#klinecandlestick-data
https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m&limit=60
### Recommendations
Use OOP approach
Imagine that in the future you have to implement few other data sources
Load data concurrently with async
Code should be production ready, well optimized, typed, with PEP8 respect



from decimal import Decimal


class IntegrationVolatilityMetric:
    def __init__(self, symbol_pair: str, volatility: Decimal):
        self.symbol_pair = symbol_pair
        self.volatility = volatility

    def __str__(self):
        return f'Symbol pair: {self.symbol_pair}, volatility: {self.volatility}'

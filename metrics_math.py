from decimal import Decimal


# Formula given in task description:
# volatility = (max_high - min_low) / min_low * 100
async def calculate_volatility(max_high: Decimal, min_low: Decimal) -> Decimal:
    return (max_high / min_low - 1) * 100

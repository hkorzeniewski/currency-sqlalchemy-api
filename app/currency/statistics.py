from decimal import Decimal
from typing import List


def calculate_average(data: List[tuple]) -> Decimal:
    if not data:
        return Decimal("0.0")

    total = sum(item[0] for item in data)
    average = round(total / len(data), 4)
    return average


def calculate_max_value(data: List[tuple]) -> Decimal:
    if not data:
        return Decimal("0.0")

    max_value = max(item[0] for item in data)
    return max_value


def calculate_min_value(data: List[tuple]) -> Decimal:
    if not data:
        return Decimal("0.0")

    min_value = min(item[0] for item in data)
    return min_value

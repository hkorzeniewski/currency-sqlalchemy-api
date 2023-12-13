from decimal import Decimal
from typing import List


def calculate_eur_usd_and_chf_usd(eur_pln: list, usd_pln: list, chf_pln: list) -> List[tuple]:
    eur_usd = []
    chf_usd = []
    for eur, usd, chf in zip(eur_pln, usd_pln, chf_pln):
        eur_usd.append(round(eur / usd, 4))
        chf_usd.append(round(chf / usd, 4))
    return eur_usd, chf_usd


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

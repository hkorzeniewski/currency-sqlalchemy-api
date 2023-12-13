from typing import Optional
from pydantic import condecimal
from sqlmodel import Field, SQLModel


class Currency(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    eur_pln: condecimal(decimal_places=4, max_digits=6)
    usd_pln: condecimal(decimal_places=4, max_digits=6)
    chf_pln: condecimal(decimal_places=4, max_digits=6)
    eur_usd: condecimal(decimal_places=4, max_digits=6)
    chf_usd: condecimal(decimal_places=4, max_digits=6)
    rate_date: str

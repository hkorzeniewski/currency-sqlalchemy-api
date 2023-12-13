from typing import List
from sqlalchemy.future import select
from fastapi import APIRouter, Depends, Query, Request
from typing import Annotated

from sqlmodel.ext.asyncio.session import AsyncSession

from app.currency.services import CurrencyService
from app.currency.models import Currency
from app.db import get_session

router = APIRouter(tags=["currency"])

currency_service = CurrencyService()


@router.get("/currencies")
async def get_currencies(request: Request):
    currencies = currency_service.get_currencies()
    return currencies


@router.get("/query_generator")
async def get_query_generator(request: Request):
    eur_pln = currency_service.get_eur_pln_rate(4)
    query = currency_service.make_query_sql_insert(eur_pln[1])
    return query


@router.get("/currencies/eur-pln")
async def get_eur_pln(session: AsyncSession = Depends(get_session)):
    eur_pln = currency_service.get_eur_pln_rate(4)
    print(eur_pln)
    eur_pln = [{"eur_pln": value} for value in eur_pln]
    session.add_all(eur_pln)
    await session.commit()
    await session.refresh(eur_pln)
    return eur_pln


@router.get("/currencies/usd-pln")
async def get_usd_pln(session: AsyncSession = Depends(get_session)):
    usd_pln = currency_service.get_currency_rate("usd", 4)
    # print(usd_pln)
    usd_pln = [{"usd_pln": value} for value in usd_pln]
    session.add_all(usd_pln)
    await session.commit()
    await session.refresh(usd_pln)
    return usd_pln


@router.post("/currencies/all")
async def post_currencies(session: AsyncSession = Depends(get_session)):
    currencies = currency_service.prepare_currencies_to_db()
    currencies_to_db = [Currency(**currency, id=i) for i, currency in enumerate(currencies)]

    print(currencies_to_db)
    session.add_all(currencies_to_db)
    await session.commit()
    return currencies


@router.get("/currencies/select_one")
async def get_currency_data(
    session: AsyncSession = Depends(get_session),
    currency_code: str = "eur_pln",
):
    financial_data = await session.execute(select(Currency.rate_date, getattr(Currency, currency_code)))
    financial_data = financial_data.all()
    return financial_data


@router.get("/currencies/select_many")
async def get_many_currency_data(
    selected_columns: Annotated[list[str] | None, Query()] = None,
    session: AsyncSession = Depends(get_session),
):
    selected_columns.append("rate_date")
    columns = [getattr(Currency, column) for column in selected_columns]
    financial_data = await session.execute(
        select(*columns)
    )
    financial_data = financial_data.all()
    return financial_data

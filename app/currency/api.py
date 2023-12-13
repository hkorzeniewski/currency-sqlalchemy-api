from fastapi import APIRouter, BackgroundTasks, Depends, Query, Request

from typing import Annotated

from sqlalchemy.future import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.logs import logger
from app.currency.constants import CurrencyCodeEnum
from app.currency.models import Currency
from app.currency.services import CurrencyService
from app.db import get_session

router = APIRouter(tags=["currency"])

currency_service = CurrencyService()


@router.get("/currencies")
async def get_currencies(request: Request):
    currencies = currency_service.get_currencies()
    return currencies

@router.post("/currencies/all")
async def post_currencies(background_tasks: BackgroundTasks, session: AsyncSession = Depends(get_session)):
    currencies = currency_service.prepare_currencies_to_db()
    currencies_to_db = [Currency(**currency, id=i) for i, currency in enumerate(currencies)]
    print(currencies_to_db)
    background_tasks.add_task(currency_service.save_all_currencies_to_csv_file, currencies)
    session.add_all(currencies_to_db)
    await session.commit()
    return currencies


@router.get("/currencies/select_one")
async def get_currency_data(
    session: AsyncSession = Depends(get_session),
    currency_code: CurrencyCodeEnum = "eur_pln",
):
    financial_data = await session.execute(select(Currency.rate_date, getattr(Currency, currency_code)))
    financial_data = financial_data.all()
    return financial_data


@router.get("/currencies/select_many")
async def get_many_currency_data(
    selected_columns: Annotated[list[CurrencyCodeEnum] | None, Query()] = None,
    session: AsyncSession = Depends(get_session),
):
    selected_columns.append("rate_date")
    columns = [getattr(Currency, column) for column in selected_columns]
    financial_data = await session.execute(select(*columns))
    financial_data = financial_data.all()
    return financial_data


@router.get("/currencies/select_many/save_to_csv")
async def get_many_currency_data_save_to_csv(
    background_tasks: BackgroundTasks,
    selected_columns: Annotated[list[CurrencyCodeEnum] | None, Query()] = None,
    session: AsyncSession = Depends(get_session),
):
    filename_csv = "_".join(column for column in selected_columns)
    logger.info(filename_csv)
    selected_columns.append("rate_date")
    columns = [getattr(Currency, column) for column in selected_columns]
    financial_data = await session.execute(select(*columns))
    financial_data = financial_data.all()
    background_tasks.add_task(
        currency_service.save_specific_currencies_to_csv_file, financial_data, selected_columns, filename_csv
    )
    return {"message": f"File {filename_csv}_currency_data.csv saved"}

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, Request

from typing import Annotated

from sqlalchemy.future import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.logs import logger
from app.currency.constants import CurrencyCodeEnum
from app.currency.models import Currency
from app.currency.services import CurrencyService
from app.currency.statistics import calculate_average, calculate_max_value, calculate_min_value
from app.currency.utils import (
    is_valid_date_format,
    save_specific_currencies_to_csv_file,
)
from app.db import get_session

router = APIRouter(tags=["currency"])

currency_service = CurrencyService()


@router.get("/currencies")
async def get_currencies(request: Request):
    currencies = currency_service.get_currencies()
    return currencies


@router.get("/currencies/select_one")
async def get_currency_data(
    session: AsyncSession = Depends(get_session),
    currency_code: CurrencyCodeEnum = "eur_pln",
):
    if currency_code not in CurrencyCodeEnum:
        raise HTTPException(status_code=404, detail="Data not found")
    financial_data = await session.execute(select(Currency.rate_date, getattr(Currency, currency_code)))
    financial_data = financial_data.all()
    if not financial_data:
        raise HTTPException(status_code=404, detail="Data not found")
    return financial_data


@router.get("/currencies/select_many")
async def get_many_currency_data(
    selected_columns: Annotated[list[CurrencyCodeEnum] | None, Query()] = None,
    session: AsyncSession = Depends(get_session),
):
    if not selected_columns:
        raise HTTPException(status_code=422, detail="No columns selected")
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
    if not selected_columns:
        raise HTTPException(status_code=422, detail="No columns selected")
    filename_csv = "_".join(column for column in selected_columns)
    logger.info(filename_csv)
    selected_columns.append("rate_date")
    columns = [getattr(Currency, column) for column in selected_columns]
    financial_data = await session.execute(select(*columns))
    financial_data = financial_data.all()
    background_tasks.add_task(save_specific_currencies_to_csv_file, financial_data, selected_columns, filename_csv)
    return {"message": f"File {filename_csv}_currency_data.csv saved"}


@router.get("/currencies/{currency_code}/average")
async def get_average_currency_rate(
    currency_code: CurrencyCodeEnum = "eur_pln",
    session: AsyncSession = Depends(get_session),
):
    data = await session.execute(select(getattr(Currency, currency_code)))
    data = data.all()
    avarage = calculate_average(data)
    logger.info(avarage)
    return {f"avarage for {currency_code}": avarage}


@router.get("/currencies/{currency_code}/maximum")
async def get_maximum_currency_rate(
    currency_code: CurrencyCodeEnum = "eur_pln",
    session: AsyncSession = Depends(get_session),
):
    data = await session.execute(select(getattr(Currency, currency_code)))
    data = data.all()
    maximum = calculate_max_value(data)
    logger.info(maximum)
    return {f"maximum for {currency_code}": maximum}


@router.get("/currencies/{currency_code}/minimum")
async def get_minimum_currency_rate(
    currency_code: CurrencyCodeEnum = "eur_pln",
    session: AsyncSession = Depends(get_session),
):
    data = await session.execute(select(getattr(Currency, currency_code)))
    data = data.all()
    minimum = calculate_min_value(data)
    logger.info(minimum)
    return {f"minimum for {currency_code}": minimum}


@router.get("/currencies/{currency_code}/date-range")
async def get_currency_rate_date_range(
    currency_code: CurrencyCodeEnum = "eur_pln",
    session: AsyncSession = Depends(get_session),
    start_date: str = Query(...),
    end_date: str = Query(...),
):
    valid_date = is_valid_date_format(start_date, end_date)
    if valid_date[0] is False:
        raise HTTPException(status_code=422, detail=f"Wrong date format {valid_date[1]}")
    data = await session.execute(
        select(Currency.rate_date, getattr(Currency, currency_code)).where(
            Currency.rate_date.between(start_date, end_date)
        )
    )
    data = data.all()
    logger.info(data)
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    return data

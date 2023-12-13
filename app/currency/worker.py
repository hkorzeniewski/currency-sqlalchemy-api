from celery import Celery
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from app.currency.models import Currency
from app.currency.services import CurrencyService
from app.db import ASYNC_DATABASE_URI, engine
from settings.base import settings

celery_app = Celery("tasks", broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND)

currency_service = CurrencyService()

session = sessionmaker(ASYNC_DATABASE_URI, class_=AsyncSession, expire_on_commit=False)


@celery_app.task
async def save_currencies_to_db():
    currencies = currency_service.prepare_currencies_to_db()
    currencies_to_db = [Currency(**currency) for currency in currencies]
    session.add(currencies_to_db)
    await session.commit()
    return currencies


@celery_app.task
async def save_today_currencies_to_db():
    try:
        eur_pln = currency_service.get_today_currency_rate("eur")
        usd_pln = currency_service.get_today_currency_rate("usd")
        chf_pln = currency_service.get_today_currency_rate("chf")
        eur_usd = eur_pln["mid"] / usd_pln["mid"]
        chf_usd = chf_pln["mid"] / usd_pln["mid"]
    except BaseException as e:
        print(e)
        raise {"message": "Error during fetching data from API"}
    currency = Currency(
        eur_pln=eur_pln["mid"],
        usd_pln=usd_pln["mid"],
        chf_pln=chf_pln["mid"],
        eur_usd=eur_usd,
        chf_usd=chf_usd,
    )
    print(currency)
    with AsyncSession(engine) as session:
        session.add(currency)
        await session.commit()
        await session.refresh(currency)

    return currency


if __name__ == "__main__":
    celery_app.start()

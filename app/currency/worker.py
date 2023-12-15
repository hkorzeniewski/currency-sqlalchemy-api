from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.currency.models import Currency
from app.currency.services import CurrencyService
from app.currency.utils import (
    save_all_currencies_to_csv_file_pandas,
    save_new_line_to_csv_file_pandas,
)
from app.db import DATABASE_URI
from settings.base import settings

celery_app = Celery("tasks", broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND)

currency_service = CurrencyService()

sync_engine = create_engine(f"postgresql://{DATABASE_URI}", echo=True)
SyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=sync_engine,
)


@celery_app.task
def save_currencies_to_db():
    currencies = currency_service.prepare_currencies_to_db()
    currencies_to_db = [Currency(**currency) for currency in currencies]
    with SyncSessionLocal() as session:
        is_data_in_db = session.query(Currency).all()
        if is_data_in_db:
            return {"message": "Data already in db"}
        session.add_all(currencies_to_db)
        session.commit()
    save_all_currencies_to_csv_file_pandas(currencies, filename="all_currency_data.csv")
    return currencies


@celery_app.task
def save_today_currencies_to_db():
    try:
        eur_pln = currency_service.get_today_currency_rate("eur")
        usd_pln = currency_service.get_today_currency_rate("usd")
        chf_pln = currency_service.get_today_currency_rate("chf")
        eur_usd = round(eur_pln["mid"] / usd_pln["mid"], 4)
        chf_usd = round(chf_pln["mid"] / usd_pln["mid"], 4)
    except BaseException as e:
        print(e)
        raise {"message": "Error during fetching data from API"}
    currency = {
        "eur_pln": eur_pln["mid"],
        "usd_pln": usd_pln["mid"],
        "chf_pln": chf_pln["mid"],
        "eur_usd": eur_usd,
        "chf_usd": chf_usd,
        "rate_date": eur_pln["effectiveDate"],
    }
    with SyncSessionLocal() as session:
        session.add(Currency(**currency))
        session.commit()
    save_new_line_to_csv_file_pandas(currency, "all_currency_data.csv")
    return {"message": "Data saved to db"}

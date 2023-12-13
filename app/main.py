from fastapi import BackgroundTasks, FastAPI, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app import version
from app.core.api import router as core_router
from app.core.logs import logger
from app.core.middlewares import apply_middlewares
from app.currency.api import router as currency_router
from app.currency.services import CurrencyService
from app.currency.worker import save_currencies_to_db
from app.db import get_session

app = FastAPI(version=version)
app = apply_middlewares(app)

app.include_router(currency_router)
app.include_router(core_router)

logger.info("App is ready!")



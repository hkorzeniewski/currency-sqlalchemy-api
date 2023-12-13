from fastapi import FastAPI

from app import version
from app.core.api import router as core_router
from app.core.logs import logger
from app.core.middlewares import apply_middlewares
from app.currency.api import router as currency_router

app = FastAPI(version=version)
app = apply_middlewares(app)

app.include_router(currency_router)
app.include_router(core_router)

logger.info("App is ready!")

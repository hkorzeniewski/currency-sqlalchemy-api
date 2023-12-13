from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware

from settings.base import settings


def add_cors_middleware(app: FastAPI) -> FastAPI:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "HEAD", "OPTIONS", "DELETE"],
        allow_headers=[
            "Access-Control-Allow-Headers",
            "Content-Type",
            "Authorization",
            "Access-Control-Allow-Origin",
            "Set-Cookie",
            "sentry-trace",
        ],
    )
    return app


MIDDLEWARES = (add_cors_middleware,)


def apply_middlewares(app: FastAPI) -> FastAPI:
    for middleware in MIDDLEWARES:
        app = middleware(app)
    return app

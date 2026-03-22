import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

LOGGER = logging.getLogger("uvicorn")


@asynccontextmanager
async def _lifespan(_: FastAPI):
    LOGGER.info("Commit quality service started. Loading model.")
    yield
    LOGGER.info("Commit quality service shutting down.")


app = FastAPI(
    title="Commit Quality Service",
    lifespan=_lifespan,
)

app.add_middleware(TrustedHostMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

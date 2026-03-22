import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, File, Response, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from feedback.models.response import Annotation

LOGGER = logging.getLogger("uvicorn")


@asynccontextmanager
async def _lifespan(_: FastAPI):
    LOGGER.info("Feedback service started. Loading model.")
    yield
    LOGGER.info("Feedback quality service shutting down.")


app = FastAPI(
    title="Feedback Service",
    lifespan=_lifespan,
)

app.add_middleware(TrustedHostMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ingest/good")
async def ingest_good(file: UploadFile = File(...)):  # noqa: B008
    return Response(status_code=200)


@app.post("/ingest/marked")
async def ingest_marked(
    file: UploadFile = File(...),  # noqa: B008
):
    return Response(status_code=200)


@app.post("/ingest/context")
async def injest_context(context: str):
    return Response(status_code=200)


@app.post("/analyse", response_model=list[Annotation])
async def analyse(file: UploadFile = File(...)):  # noqa: B008
    return [
        Annotation(
            span="The play ends happily.",
            comment="Oversimplified. Resolution is more ambiguous than stated.",
        ),
    ]

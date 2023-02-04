from fastapi import FastAPI
from fastapi_utils.timing import add_timing_middleware
from starlette.responses import JSONResponse

from app import __version__, score, train
from app.constants import NAME, PATH_PREFIX
from app.log import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title=NAME.title(),
    docs_url=f"{PATH_PREFIX}/docs",
    redoc_url=f"{PATH_PREFIX}/redoc",
    openapi_url=f"{PATH_PREFIX}/openapi.json",
)

add_timing_middleware(app, record=logger.info)

app.include_router(score.router, prefix=PATH_PREFIX)
app.include_router(train.router, prefix=PATH_PREFIX)


@app.get(PATH_PREFIX)
async def root():
    return JSONResponse(content={"status": "available"})


@app.get(f"{PATH_PREFIX}/health")
async def health():
    return JSONResponse(content={"status": "available"})


@app.get(f"{PATH_PREFIX}/version")
async def version():
    return JSONResponse(content={"version": "__version__"})

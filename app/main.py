from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.database import clickhouse_client
from app.routers import test

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    clickhouse_client.disconnect()

app = FastAPI(title="ClickHouse FastAPI", lifespan=lifespan)

app.include_router(test.router, tags=["test"])

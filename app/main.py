from fastapi import FastAPI
from app.routers import test, concurrent, deals

app = FastAPI()

app.include_router(test.router)
app.include_router(concurrent.router)
app.include_router(deals.router)


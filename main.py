from fastapi import FastAPI
from router.api import router
from test import app as router1

app=FastAPI()
# app.include_router(router,prefix="/api")
app.include_router(router1,prefix="/oolama")
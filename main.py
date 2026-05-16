from fastapi import FastAPI
from router.api import router   
from test import app as test_app
app=FastAPI()
app.include_router(router,prefix="/api")
app.include_router(test_app,prefix="/oolama")
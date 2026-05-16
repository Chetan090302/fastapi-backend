import asyncio
import time
from fastapi import APIRouter
from pydantic import BaseModel
# from model import trigger_rag_document


router=APIRouter()

class Input(BaseModel):
    query:str=None

@router.post("/data")
async def get_data(input:Input):
    await asyncio.sleep(1)
    input_data=input.model_dump()
    query=input_data.get("query")
    response=await asyncio.to_thread(blo_data,query)
    return response

@router.get("/health")
async def get_health():
    start_time=time.time()
    response=await asyncio.to_thread(get_health_data)
    end_time=time.time()
    print(f"Time taken to get health data: {end_time-start_time} seconds")
    return response

def blo_data(input_query):
    return {"response":input_query}

def get_health_data():
    time.sleep(3)
    return {"status":"ok"}
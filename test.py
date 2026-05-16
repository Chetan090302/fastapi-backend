import ollama
import asyncio
from fastapi import FastAPI,APIRouter,Request
from pydantic import BaseModel
import json
from fastapi.responses import JSONResponse,StreamingResponse

class Input(BaseModel):
    input_query:str

app = APIRouter()

def call_model(user_input:str):
    return ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": f"{user_input}"}]
    )

@app.post("/chat")
async def chat(input:Input):
    input_dict=input.model_dump()
    response = await asyncio.to_thread(call_model,input_dict.get("input_query"))
    return {"response": response['message']['content']}

@app.post("/test")
async def testing_method(request:Request):
    input_data = await request.json()
    return StreamingResponse(
        fake_llm_call(input_data),
        media_type="text/event-stream",
        status_code=200,
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )

async def fake_llm_call(input_data=None):
    for i in range(5):
        chunk = f"data: Message {i}\n\n"
        yield chunk.encode("utf-8")
        await asyncio.sleep(5)

async def main_method():
    input_data=["capital of france","capital of germany","capital of italy"]
    response=asyncio.map(call_model,input_data)
    return response


#hello world


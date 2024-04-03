from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


class Numbers(BaseModel):
    a: int
    b: int

@app.post("/sum")
async def calculate_sum(numbers: Numbers):
    result = numbers.a + numbers.b
    return {"sum": result}
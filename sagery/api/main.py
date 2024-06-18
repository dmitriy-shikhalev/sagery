import logging

from fastapi import FastAPI

app = FastAPI()
logging.basicConfig(level=logging.INFO)


@app.get("/")
async def root():
    return {"message": "Hello World"}
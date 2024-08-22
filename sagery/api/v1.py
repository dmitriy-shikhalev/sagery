from fastapi import FastAPI


app = FastAPI(title='Sagery API')


@app.get("/")
async def root():
    return {"message": "Hello World"}

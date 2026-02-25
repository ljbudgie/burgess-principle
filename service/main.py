from fastapi import FastAPI

app = FastAPI()

@app.get("/xai-hybrid-core")
async def read_root():
    return {"message": "Welcome to the xAI-Hybrid Core public endpoint!"}

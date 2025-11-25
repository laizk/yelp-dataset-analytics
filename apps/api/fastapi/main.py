from fastapi import FastAPI
from api.routes import router as api_router

app = FastAPI(title='Yelp Dataset Analytics API')

app.include_router(api_router, prefix='/api')

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}
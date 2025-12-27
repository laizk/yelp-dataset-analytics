from fastapi import FastAPI
from api.routes import kafka_router, business_router, user_router
from core.config import get_settings

settings = get_settings()

app = FastAPI(title=settings.APP_NAME)

# All API routes are under /api
app.include_router(kafka_router, prefix="/api")
app.include_router(business_router, prefix="/api")
app.include_router(user_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}

from fastapi import FastAPI

from app.api.router import api_router
from config import app_info, settings

app = FastAPI(title=app_info.name, debug=settings.debug, version=app_info.version)


@app.get("/health", tags=["system"])
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(api_router, prefix="/api/v1")

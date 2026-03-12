from fastapi import FastAPI

from app.core.config import get_settings


settings = get_settings()

app = FastAPI(title=settings.app_name)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

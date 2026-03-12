from fastapi import FastAPI

from app.core.config import get_settings
from app.modules.auth.router import router as auth_router


settings = get_settings()

app = FastAPI(title=settings.app_name)
app.include_router(auth_router)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

from fastapi import FastAPI

from app.core.config import get_settings
from app.modules.auth.router import router as auth_router
from app.modules.backtests.router import router as backtests_router
from app.modules.market_data.router import router as market_data_router
from app.modules.results.router import router as results_router
from app.modules.strategies.router import router as strategies_router


settings = get_settings()

app = FastAPI(title=settings.app_name)
app.include_router(auth_router)
app.include_router(backtests_router)
app.include_router(market_data_router)
app.include_router(results_router)
app.include_router(strategies_router)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

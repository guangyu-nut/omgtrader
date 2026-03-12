# A 股量化回测网站 MVP Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a macOS-local A-share backtesting website MVP that supports local login, market data sync, stock-pool rotation strategy configuration, minute-bar execution simulation, result visualization, strategy persistence, and AI-assisted interpretation.

**Architecture:** Implement a local-first monolith with a Vue 3 frontend, a FastAPI backend, SQLite as the default database, and a self-owned backtesting engine module. Keep market data, strategy configuration, backtest execution, results, and AI assistance in separate bounded modules so the MVP can grow without being rewritten.

**Tech Stack:** Vue 3, Vite, TypeScript, Python 3.11+, FastAPI, SQLAlchemy, Alembic, Pydantic, pytest, Vitest, Playwright, SQLite, ECharts

---

## Spec Reference

- Spec: `docs/superpowers/specs/2026-03-12-a-share-backtesting-web-design.md`

## File Structure Map

The implementation should create the following top-level structure and keep responsibilities narrow:

- `backend/pyproject.toml`
  - Python dependencies and tool configuration
- `backend/alembic.ini`
  - Alembic entrypoint
- `backend/alembic/versions/*.py`
  - Database migrations
- `backend/app/main.py`
  - FastAPI application bootstrap
- `backend/app/core/config.py`
  - Environment and app settings
- `backend/app/core/database.py`
  - Engine, session factory, metadata wiring
- `backend/app/core/security.py`
  - Password hashing and session token helpers
- `backend/app/modules/auth/*`
  - User, session, login endpoints
- `backend/app/modules/market_data/*`
  - Symbols, bars, calendars, data sources, sync tasks
- `backend/app/modules/strategies/*`
  - Strategy templates, stock pools, execution settings
- `backend/app/modules/backtests/*`
  - Snapshot creation, backtest jobs, execution orchestration
- `backend/app/modules/results/*`
  - Curves, metrics, orders, trades, positions, query endpoints
- `backend/app/modules/ai_assistant/*`
  - AI request assembly and persistence of AI insights
- `backend/app/services/data_providers/*`
  - Provider interfaces and concrete adapters
- `backend/app/services/backtest_engine/*`
  - Domain engine for signal generation, execution simulation, metrics
- `backend/tests/*`
  - Backend unit, integration, and API tests
- `frontend/package.json`
  - Frontend dependencies and scripts
- `frontend/vite.config.ts`
  - Vite configuration
- `frontend/src/main.ts`
  - Frontend bootstrap
- `frontend/src/router.ts`
  - Route definitions
- `frontend/src/api/*`
  - Typed API client modules
- `frontend/src/stores/*`
  - UI state stores
- `frontend/src/views/*`
  - Page-level screens
- `frontend/src/components/*`
  - Reusable focused components
- `frontend/src/charts/*`
  - ECharts option factories
- `frontend/src/types/*`
  - Shared frontend DTOs
- `frontend/src/tests/*`
  - Component and view tests
- `e2e/tests/*`
  - End-to-end flow tests
- `scripts/dev/start.sh`
  - One-command local startup
- `scripts/dev/seed_demo_data.py`
  - Local seed helper for demos and tests
- `docs/runbooks/local-setup.md`
  - Local startup and troubleshooting guide

## Implementation Order

Build in this order to keep every intermediate state testable:

1. Project skeleton and local startup
2. Local auth and persistence foundation
3. Market data ingestion and health visibility
4. Strategy assets and configuration APIs
5. Backtest snapshotting and engine MVP
6. Result visualization and history reuse
7. AI interpretation and local startup polish

## Chunk 1: Foundation And Local Startup

### Task 1: Scaffold backend service and test harness

**Files:**
- Create: `backend/pyproject.toml`
- Create: `backend/app/main.py`
- Create: `backend/app/core/config.py`
- Create: `backend/app/core/database.py`
- Create: `backend/tests/conftest.py`
- Create: `backend/tests/test_health_api.py`

- [ ] **Step 1: Write the failing backend health test**

```python
from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint_returns_ok():
    client = TestClient(app)
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

- [ ] **Step 2: Run the test to verify the app is not ready**

Run: `cd backend && pytest tests/test_health_api.py -v`
Expected: FAIL with import error or missing `/api/health` route

- [ ] **Step 3: Implement the minimal FastAPI bootstrap**

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
```

- [ ] **Step 4: Re-run the health test**

Run: `cd backend && pytest tests/test_health_api.py -v`
Expected: PASS

- [ ] **Step 5: Commit the backend scaffold**

```bash
git add backend
git commit -m "chore: scaffold backend service"
```

### Task 2: Scaffold frontend shell and route smoke test

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/vite.config.ts`
- Create: `frontend/src/main.ts`
- Create: `frontend/src/router.ts`
- Create: `frontend/src/App.vue`
- Create: `frontend/src/views/LoginView.vue`
- Create: `frontend/src/tests/router.spec.ts`

- [ ] **Step 1: Write the failing frontend route test**

```ts
import { describe, expect, it } from "vitest";
import { router } from "../router";

describe("router", () => {
  it("registers the login route", () => {
    expect(router.resolve("/login").name).toBe("login");
  });
});
```

- [ ] **Step 2: Run the frontend test before scaffolding**

Run: `cd frontend && npm test -- --run src/tests/router.spec.ts`
Expected: FAIL because the frontend project or router does not exist

- [ ] **Step 3: Implement the minimal Vite + Vue shell**

```ts
import { createRouter, createWebHistory } from "vue-router";

export const router = createRouter({
  history: createWebHistory(),
  routes: [{ path: "/login", name: "login", component: () => import("./views/LoginView.vue") }],
});
```

- [ ] **Step 4: Re-run the route test**

Run: `cd frontend && npm test -- --run src/tests/router.spec.ts`
Expected: PASS

- [ ] **Step 5: Commit the frontend scaffold**

```bash
git add frontend
git commit -m "chore: scaffold frontend app"
```

### Task 3: Add one-command local startup wiring

**Files:**
- Create: `scripts/dev/start.sh`
- Create: `docs/runbooks/local-setup.md`
- Create: `e2e/tests/smoke-startup.spec.ts`

- [ ] **Step 1: Write the failing startup smoke test**

```ts
import { test, expect } from "@playwright/test";

test("login page renders on local startup", async ({ page }) => {
  await page.goto("http://127.0.0.1:5173/login");
  await expect(page.getByRole("heading", { name: "登录" })).toBeVisible();
});
```

- [ ] **Step 2: Run the smoke test before the script exists**

Run: `cd frontend && npx playwright test ../e2e/tests/smoke-startup.spec.ts`
Expected: FAIL because the frontend/backend processes are not bootstrapped

- [ ] **Step 3: Implement the startup script and runbook**

```bash
#!/usr/bin/env bash
set -euo pipefail

cd backend && uv run uvicorn app.main:app --reload &
cd ../frontend && npm run dev -- --host 127.0.0.1
```

- [ ] **Step 4: Start the stack and re-run the smoke test**

Run: `bash scripts/dev/start.sh`
Run: `cd frontend && npx playwright test ../e2e/tests/smoke-startup.spec.ts`
Expected: PASS with the login page visible

- [ ] **Step 5: Commit the local startup flow**

```bash
git add scripts docs/runbooks e2e
git commit -m "chore: add local startup flow"
```

## Chunk 2: Auth, Schema, And Data Sync Foundation

### Task 4: Create database schema foundation and migrations

**Files:**
- Create: `backend/alembic.ini`
- Create: `backend/alembic/env.py`
- Create: `backend/alembic/versions/0001_initial_core_tables.py`
- Create: `backend/app/modules/auth/models.py`
- Create: `backend/app/modules/market_data/models.py`
- Create: `backend/app/modules/strategies/models.py`
- Create: `backend/app/modules/backtests/models.py`
- Create: `backend/app/modules/results/models.py`
- Create: `backend/tests/test_migrations.py`

- [ ] **Step 1: Write the failing migration test**

```python
from sqlalchemy import inspect


def test_initial_migration_creates_core_tables(db_engine):
    tables = set(inspect(db_engine).get_table_names())

    assert {"users", "symbols", "bar_daily", "bar_minute", "strategy_instances", "backtest_jobs"} <= tables
```

- [ ] **Step 2: Run the migration test before migrations exist**

Run: `cd backend && pytest tests/test_migrations.py -v`
Expected: FAIL because the schema and migration wiring are missing

- [ ] **Step 3: Implement the initial models and Alembic migration**

```python
class User(Base):
    __tablename__ = "users"
    id = mapped_column(UUID, primary_key=True)


class Symbol(Base):
    __tablename__ = "symbols"
    id = mapped_column(UUID, primary_key=True)
```

- [ ] **Step 4: Run migrations and re-run the test**

Run: `cd backend && alembic upgrade head`
Run: `cd backend && pytest tests/test_migrations.py -v`
Expected: PASS

- [ ] **Step 5: Commit the schema foundation**

```bash
git add backend
git commit -m "feat: add core schema foundation"
```

### Task 5: Implement local login and session APIs

**Files:**
- Create: `backend/app/core/security.py`
- Create: `backend/app/modules/auth/schemas.py`
- Create: `backend/app/modules/auth/repository.py`
- Create: `backend/app/modules/auth/service.py`
- Create: `backend/app/modules/auth/router.py`
- Modify: `backend/app/main.py`
- Create: `backend/tests/modules/auth/test_login_api.py`
- Create: `frontend/src/api/auth.ts`
- Create: `frontend/src/stores/auth.ts`
- Create: `frontend/src/views/LoginView.vue`
- Create: `frontend/src/tests/login-view.spec.ts`

- [ ] **Step 1: Write the failing backend login API test**

```python
def test_login_returns_session_token(client, seeded_user):
    response = client.post("/api/auth/login", json={"username": "demo", "password": "pass123456"})

    assert response.status_code == 200
    assert "token" in response.json()
```

- [ ] **Step 2: Run the backend auth test**

Run: `cd backend && pytest tests/modules/auth/test_login_api.py -v`
Expected: FAIL because the auth route and session logic are missing

- [ ] **Step 3: Implement password hashing, session storage, and the login endpoint**

```python
@router.post("/login")
def login(payload: LoginRequest, service: AuthService = Depends(get_auth_service)) -> LoginResponse:
    return service.login(payload.username, payload.password)
```

- [ ] **Step 4: Re-run the backend auth test**

Run: `cd backend && pytest tests/modules/auth/test_login_api.py -v`
Expected: PASS

- [ ] **Step 5: Write the failing frontend login view test**

```ts
it("submits credentials and stores the session", async () => {
  render(LoginView);
  await user.type(screen.getByLabelText("用户名"), "demo");
  await user.type(screen.getByLabelText("密码"), "pass123456");
  await user.click(screen.getByRole("button", { name: "登录" }));

  expect(authStore.token).toBe("session-token");
});
```

- [ ] **Step 6: Run the frontend login test before wiring the form**

Run: `cd frontend && npm test -- --run src/tests/login-view.spec.ts`
Expected: FAIL because the form submission/store integration is missing

- [ ] **Step 7: Implement the login page flow**

```ts
const onSubmit = async () => {
  await authStore.login(form.username, form.password);
  router.push("/");
};
```

- [ ] **Step 8: Re-run the frontend login test**

Run: `cd frontend && npm test -- --run src/tests/login-view.spec.ts`
Expected: PASS

- [ ] **Step 9: Commit local auth**

```bash
git add backend frontend
git commit -m "feat: add local login flow"
```

### Task 6: Implement data source configuration and sync task tracking

**Files:**
- Create: `backend/app/modules/market_data/schemas.py`
- Create: `backend/app/modules/market_data/repository.py`
- Create: `backend/app/modules/market_data/service.py`
- Create: `backend/app/modules/market_data/router.py`
- Create: `backend/app/services/data_providers/base.py`
- Create: `backend/app/services/data_providers/free_source.py`
- Create: `backend/app/services/data_providers/token_source.py`
- Create: `backend/tests/modules/market_data/test_data_sources_api.py`
- Create: `backend/tests/modules/market_data/test_sync_tasks_api.py`

- [ ] **Step 1: Write the failing data source API test**

```python
def test_create_data_source_config(client, auth_headers):
    response = client.post(
        "/api/market-data/data-sources",
        headers=auth_headers,
        json={"name": "free-default", "provider_type": "free", "enabled": True},
    )

    assert response.status_code == 201
    assert response.json()["provider_type"] == "free"
```

- [ ] **Step 2: Run the data source test**

Run: `cd backend && pytest tests/modules/market_data/test_data_sources_api.py -v`
Expected: FAIL because market-data APIs are missing

- [ ] **Step 3: Implement data source CRUD and sync task records**

```python
@router.post("/data-sources", status_code=201)
def create_data_source(payload: DataSourceCreate, service: MarketDataService = Depends(get_market_data_service)):
    return service.create_data_source(payload)
```

- [ ] **Step 4: Re-run the API tests**

Run: `cd backend && pytest tests/modules/market_data/test_data_sources_api.py tests/modules/market_data/test_sync_tasks_api.py -v`
Expected: PASS

- [ ] **Step 5: Commit market data source management**

```bash
git add backend
git commit -m "feat: add data source management"
```

### Task 7: Add symbol, calendar, and bar ingestion services

**Files:**
- Create: `backend/app/modules/market_data/ingestion.py`
- Create: `backend/app/modules/market_data/validators.py`
- Create: `backend/tests/modules/market_data/test_ingestion_service.py`
- Create: `backend/tests/modules/market_data/test_data_coverage_api.py`
- Create: `scripts/dev/seed_demo_data.py`

- [ ] **Step 1: Write the failing ingestion service test**

```python
def test_sync_daily_and_minute_bars_updates_coverage(ingestion_service, fake_provider):
    result = ingestion_service.sync_symbol_bars(symbol="000001.SZ", provider=fake_provider)

    assert result.daily_rows > 0
    assert result.minute_rows > 0
    assert result.coverage.symbol == "000001.SZ"
```

- [ ] **Step 2: Run the ingestion tests before implementation**

Run: `cd backend && pytest tests/modules/market_data/test_ingestion_service.py tests/modules/market_data/test_data_coverage_api.py -v`
Expected: FAIL because ingestion and coverage aggregation are missing

- [ ] **Step 3: Implement ingestion, validation, and coverage updates**

```python
result = provider.fetch_bars(symbol=symbol, start=start, end=end)
validator.assert_no_duplicate_timestamps(result.minute_bars)
repository.upsert_bars(result)
repository.upsert_coverage(result.coverage_summary())
```

- [ ] **Step 4: Re-run the ingestion tests**

Run: `cd backend && pytest tests/modules/market_data/test_ingestion_service.py tests/modules/market_data/test_data_coverage_api.py -v`
Expected: PASS

- [ ] **Step 5: Commit market data ingestion**

```bash
git add backend scripts/dev
git commit -m "feat: add market data ingestion pipeline"
```

## Chunk 3: Strategy Assets And Backtest Engine MVP

### Task 8: Implement stock pool and strategy asset APIs

**Files:**
- Create: `backend/app/modules/strategies/schemas.py`
- Create: `backend/app/modules/strategies/repository.py`
- Create: `backend/app/modules/strategies/service.py`
- Create: `backend/app/modules/strategies/router.py`
- Create: `backend/tests/modules/strategies/test_stock_pools_api.py`
- Create: `backend/tests/modules/strategies/test_strategy_instances_api.py`

- [ ] **Step 1: Write the failing stock pool API test**

```python
def test_create_stock_pool_with_manual_symbols(client, auth_headers):
    response = client.post(
        "/api/strategies/stock-pools",
        headers=auth_headers,
        json={"name": "CSI300 manual", "input_mode": "manual", "symbols": ["000001.SZ", "600000.SH"]},
    )

    assert response.status_code == 201
    assert response.json()["symbols"] == ["000001.SZ", "600000.SH"]
```

- [ ] **Step 2: Run the strategy asset tests**

Run: `cd backend && pytest tests/modules/strategies/test_stock_pools_api.py tests/modules/strategies/test_strategy_instances_api.py -v`
Expected: FAIL because the strategy module is missing

- [ ] **Step 3: Implement stock pools, execution config, and strategy instance APIs**

```python
class StrategyInstanceCreate(BaseModel):
    template_type: Literal["top_n_equal_weight"]
    stock_pool_id: UUID
    ranking_metric: str
    hold_count: int
```

- [ ] **Step 4: Re-run the strategy asset tests**

Run: `cd backend && pytest tests/modules/strategies/test_stock_pools_api.py tests/modules/strategies/test_strategy_instances_api.py -v`
Expected: PASS

- [ ] **Step 5: Commit strategy asset management**

```bash
git add backend
git commit -m "feat: add strategy asset APIs"
```

### Task 9: Implement signal generation and snapshot creation

**Files:**
- Create: `backend/app/modules/backtests/schemas.py`
- Create: `backend/app/modules/backtests/repository.py`
- Create: `backend/app/modules/backtests/service.py`
- Create: `backend/app/services/backtest_engine/signals.py`
- Create: `backend/app/services/backtest_engine/snapshots.py`
- Create: `backend/tests/modules/backtests/test_snapshot_service.py`
- Create: `backend/tests/services/backtest_engine/test_signal_generation.py`

- [ ] **Step 1: Write the failing signal generation test**

```python
def test_top_n_equal_weight_signal_selects_highest_ranked_symbols(signal_service, ranked_daily_inputs):
    signal = signal_service.generate(rebalance_date="2025-01-03", strategy=top_n_strategy, daily_inputs=ranked_daily_inputs)

    assert signal.target_symbols == ["600000.SH", "000001.SZ"]
```

- [ ] **Step 2: Run the engine tests before implementation**

Run: `cd backend && pytest tests/services/backtest_engine/test_signal_generation.py tests/modules/backtests/test_snapshot_service.py -v`
Expected: FAIL because the signal and snapshot services do not exist

- [ ] **Step 3: Implement signal generation and immutable snapshots**

```python
snapshot = BacktestSnapshot.from_strategy(strategy_instance, stock_pool, execution_config, benchmark, data_version)
signal = signal_service.generate(snapshot=snapshot, daily_inputs=daily_inputs)
```

- [ ] **Step 4: Re-run the engine tests**

Run: `cd backend && pytest tests/services/backtest_engine/test_signal_generation.py tests/modules/backtests/test_snapshot_service.py -v`
Expected: PASS

- [ ] **Step 5: Commit signal and snapshot logic**

```bash
git add backend
git commit -m "feat: add signal and snapshot services"
```

### Task 10: Implement minute-bar execution simulator

**Files:**
- Create: `backend/app/services/backtest_engine/execution.py`
- Create: `backend/app/services/backtest_engine/fees.py`
- Create: `backend/app/services/backtest_engine/limits.py`
- Create: `backend/tests/services/backtest_engine/test_execution_simulator.py`

- [ ] **Step 1: Write the failing execution test**

```python
def test_execution_simulator_applies_slippage_and_price_limits(execution_service, minute_bars):
    trade = execution_service.execute_buy(
        symbol="000001.SZ",
        signal_time="2025-01-06",
        minute_bars=minute_bars,
        slippage_bps=15,
    )

    assert trade.status == "filled"
    assert trade.price > minute_bars[0].open
```

- [ ] **Step 2: Run the execution engine tests**

Run: `cd backend && pytest tests/services/backtest_engine/test_execution_simulator.py -v`
Expected: FAIL because the simulator is missing

- [ ] **Step 3: Implement minute-window execution with fees and limit checks**

```python
candidate_bar = pick_first_tradeable_bar(minute_bars)
price = apply_slippage(candidate_bar.open, slippage_bps)
limits.assert_tradeable(candidate_bar, order_side="buy")
return TradeFill(status="filled", price=price)
```

- [ ] **Step 4: Re-run the execution engine tests**

Run: `cd backend && pytest tests/services/backtest_engine/test_execution_simulator.py -v`
Expected: PASS

- [ ] **Step 5: Commit the execution simulator**

```bash
git add backend
git commit -m "feat: add minute-bar execution simulator"
```

### Task 11: Implement end-to-end backtest job orchestration

**Files:**
- Create: `backend/app/services/backtest_engine/portfolio.py`
- Create: `backend/app/services/backtest_engine/metrics.py`
- Modify: `backend/app/modules/backtests/service.py`
- Create: `backend/app/modules/backtests/router.py`
- Create: `backend/tests/modules/backtests/test_backtest_jobs_api.py`
- Create: `backend/tests/modules/backtests/test_backtest_run_integration.py`

- [ ] **Step 1: Write the failing backtest API test**

```python
def test_run_backtest_creates_job_and_metrics(client, auth_headers, seeded_strategy):
    response = client.post("/api/backtests/jobs", headers=auth_headers, json={"strategy_instance_id": seeded_strategy.id})

    assert response.status_code == 201
    assert response.json()["status"] == "completed"
    assert response.json()["metrics"]["total_return"] is not None
```

- [ ] **Step 2: Run the backtest API and integration tests**

Run: `cd backend && pytest tests/modules/backtests/test_backtest_jobs_api.py tests/modules/backtests/test_backtest_run_integration.py -v`
Expected: FAIL because orchestration and result persistence are incomplete

- [ ] **Step 3: Implement job creation, orchestration, persistence, and logs**

```python
job = repository.create_job(snapshot_id=snapshot.id, status="running")
result = engine.run(snapshot)
repository.complete_job(job.id, result=result)
```

- [ ] **Step 4: Re-run the backtest tests**

Run: `cd backend && pytest tests/modules/backtests/test_backtest_jobs_api.py tests/modules/backtests/test_backtest_run_integration.py -v`
Expected: PASS

- [ ] **Step 5: Commit the backtest orchestration**

```bash
git add backend
git commit -m "feat: add backtest job orchestration"
```

## Chunk 4: Results UI, AI Assistance, And Release Readiness

### Task 12: Implement result query APIs and result page UI

**Files:**
- Modify: `backend/app/modules/results/models.py`
- Create: `backend/app/modules/results/schemas.py`
- Create: `backend/app/modules/results/repository.py`
- Create: `backend/app/modules/results/service.py`
- Create: `backend/app/modules/results/router.py`
- Create: `backend/tests/modules/results/test_results_api.py`
- Create: `frontend/src/api/results.ts`
- Create: `frontend/src/charts/equityCurveOptions.ts`
- Create: `frontend/src/views/ResultsView.vue`
- Create: `frontend/src/components/results/MetricsCards.vue`
- Create: `frontend/src/components/results/RebalanceTable.vue`
- Create: `frontend/src/tests/results-view.spec.ts`

- [ ] **Step 1: Write the failing results API test**

```python
def test_get_backtest_result_returns_curve_and_metrics(client, auth_headers, completed_job):
    response = client.get(f"/api/results/backtests/{completed_job.id}", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["metrics"]["max_drawdown"] is not None
    assert len(response.json()["equity_curve"]) > 0
```

- [ ] **Step 2: Run the backend results tests**

Run: `cd backend && pytest tests/modules/results/test_results_api.py -v`
Expected: FAIL because result query APIs are missing

- [ ] **Step 3: Implement result query endpoints and focused DTOs**

```python
class BacktestResultDetail(BaseModel):
    metrics: MetricsDto
    equity_curve: list[CurvePointDto]
    rebalances: list[RebalanceDto]
```

- [ ] **Step 4: Re-run the backend results tests**

Run: `cd backend && pytest tests/modules/results/test_results_api.py -v`
Expected: PASS

- [ ] **Step 5: Write the failing frontend results page test**

```ts
it("renders metrics and equity curve data", async () => {
  render(ResultsView);
  expect(await screen.findByText("最大回撤")).toBeVisible();
  expect(await screen.findByText("累计收益")).toBeVisible();
});
```

- [ ] **Step 6: Run the frontend results page test**

Run: `cd frontend && npm test -- --run src/tests/results-view.spec.ts`
Expected: FAIL because the results screen is missing

- [ ] **Step 7: Implement the result page**

```ts
const { data } = await resultsApi.getBacktestResult(jobId);
curveOptions.value = buildEquityCurveOptions(data.equity_curve, data.benchmark_curve);
```

- [ ] **Step 8: Re-run the frontend results page test**

Run: `cd frontend && npm test -- --run src/tests/results-view.spec.ts`
Expected: PASS

- [ ] **Step 9: Commit result queries and UI**

```bash
git add backend frontend
git commit -m "feat: add result visualization flow"
```

### Task 13: Implement workbench and backtest center UI flows

**Files:**
- Create: `frontend/src/api/backtests.ts`
- Create: `frontend/src/views/WorkbenchView.vue`
- Create: `frontend/src/views/BacktestCenterView.vue`
- Create: `frontend/src/components/workbench/RecentRunsPanel.vue`
- Create: `frontend/src/components/workbench/DataStatusPanel.vue`
- Create: `frontend/src/components/backtests/BacktestLaunchCard.vue`
- Create: `frontend/src/components/backtests/BacktestJobTable.vue`
- Create: `frontend/src/tests/workbench-view.spec.ts`
- Create: `frontend/src/tests/backtest-center-view.spec.ts`

- [ ] **Step 1: Write the failing workbench and backtest center tests**

```ts
it("shows recent backtest summaries on the workbench", async () => {
  render(WorkbenchView);
  expect(await screen.findByText("最近回测")).toBeVisible();
});
```

```ts
it("launches a backtest job from the backtest center", async () => {
  render(BacktestCenterView);
  expect(await screen.findByRole("button", { name: "开始回测" })).toBeVisible();
});
```

- [ ] **Step 2: Run the workbench and backtest center tests**

Run: `cd frontend && npm test -- --run src/tests/workbench-view.spec.ts src/tests/backtest-center-view.spec.ts`
Expected: FAIL because the workbench and backtest center pages are missing

- [ ] **Step 3: Implement the workbench and backtest center pages**

```ts
await backtestStore.loadRecentJobs();
await backtestStore.runJob({ strategyInstanceId });
```

- [ ] **Step 4: Re-run the workbench and backtest center tests**

Run: `cd frontend && npm test -- --run src/tests/workbench-view.spec.ts src/tests/backtest-center-view.spec.ts`
Expected: PASS

- [ ] **Step 5: Commit the workbench and backtest center views**

```bash
git add frontend
git commit -m "feat: add workbench and backtest center views"
```

### Task 14: Implement data center and strategy center UI flows

**Files:**
- Create: `frontend/src/api/marketData.ts`
- Create: `frontend/src/api/strategies.ts`
- Create: `frontend/src/views/DataCenterView.vue`
- Create: `frontend/src/views/StrategyCenterView.vue`
- Create: `frontend/src/components/data/DataSourceForm.vue`
- Create: `frontend/src/components/data/SyncTaskTable.vue`
- Create: `frontend/src/components/strategies/StockPoolEditor.vue`
- Create: `frontend/src/components/strategies/StrategyForm.vue`
- Create: `frontend/src/tests/data-center-view.spec.ts`
- Create: `frontend/src/tests/strategy-center-view.spec.ts`

- [ ] **Step 1: Write the failing data center and strategy center tests**

```ts
it("shows data source status rows", async () => {
  render(DataCenterView);
  expect(await screen.findByText("最近更新时间")).toBeVisible();
});
```

```ts
it("creates a top-n equal weight strategy", async () => {
  render(StrategyCenterView);
  expect(await screen.findByText("Top N 等权轮动")).toBeVisible();
});
```

- [ ] **Step 2: Run the frontend workflow tests**

Run: `cd frontend && npm test -- --run src/tests/data-center-view.spec.ts src/tests/strategy-center-view.spec.ts`
Expected: FAIL because the workflow views are missing

- [ ] **Step 3: Implement the data center and strategy center pages**

```ts
await marketDataStore.loadDataSources();
await strategyStore.createStrategy({
  templateType: "top_n_equal_weight",
  holdCount: 10,
});
```

- [ ] **Step 4: Re-run the workflow tests**

Run: `cd frontend && npm test -- --run src/tests/data-center-view.spec.ts src/tests/strategy-center-view.spec.ts`
Expected: PASS

- [ ] **Step 5: Commit the workflow views**

```bash
git add frontend
git commit -m "feat: add data and strategy workflow views"
```

### Task 15: Implement AI insight API and UI panel

**Files:**
- Create: `backend/app/modules/ai_assistant/schemas.py`
- Create: `backend/app/modules/ai_assistant/repository.py`
- Create: `backend/app/modules/ai_assistant/service.py`
- Create: `backend/app/modules/ai_assistant/router.py`
- Create: `backend/tests/modules/ai_assistant/test_ai_insights_api.py`
- Create: `frontend/src/api/ai.ts`
- Create: `frontend/src/components/results/AiInsightPanel.vue`
- Create: `frontend/src/tests/ai-insight-panel.spec.ts`

- [ ] **Step 1: Write the failing AI insight API test**

```python
def test_generate_ai_insight_persists_result(client, auth_headers, completed_job):
    response = client.post(f"/api/ai/backtests/{completed_job.id}/insights", headers=auth_headers)

    assert response.status_code == 201
    assert "summary" in response.json()
```

- [ ] **Step 2: Run the backend AI tests**

Run: `cd backend && pytest tests/modules/ai_assistant/test_ai_insights_api.py -v`
Expected: FAIL because the AI module is missing

- [ ] **Step 3: Implement AI insight request assembly with provider abstraction**

```python
prompt = prompt_builder.build_backtest_summary(result=result, metrics=metrics)
ai_output = provider.generate(prompt)
repository.save_insight(job_id=job_id, output=ai_output)
```

- [ ] **Step 4: Re-run the backend AI tests**

Run: `cd backend && pytest tests/modules/ai_assistant/test_ai_insights_api.py -v`
Expected: PASS

- [ ] **Step 5: Write the failing AI insight panel test**

```ts
it("shows generated insight content", async () => {
  render(AiInsightPanel);
  expect(await screen.findByText("策略总结")).toBeVisible();
});
```

- [ ] **Step 6: Run the frontend AI panel test**

Run: `cd frontend && npm test -- --run src/tests/ai-insight-panel.spec.ts`
Expected: FAIL because the panel is missing

- [ ] **Step 7: Implement the AI insight panel**

```ts
const insight = await aiApi.generateInsight(jobId);
panelState.summary = insight.summary;
```

- [ ] **Step 8: Re-run the frontend AI panel test**

Run: `cd frontend && npm test -- --run src/tests/ai-insight-panel.spec.ts`
Expected: PASS

- [ ] **Step 9: Commit AI assistance**

```bash
git add backend frontend
git commit -m "feat: add AI insight assistance"
```

### Task 16: Add end-to-end regression checks and release checklist

**Files:**
- Create: `e2e/tests/backtest-happy-path.spec.ts`
- Modify: `docs/runbooks/local-setup.md`
- Create: `docs/runbooks/release-checklist.md`

- [ ] **Step 1: Write the failing end-to-end happy path test**

```ts
test("user can login, sync demo data, run backtest, and view results", async ({ page }) => {
  await page.goto("/login");
  await page.getByLabel("用户名").fill("demo");
  await page.getByLabel("密码").fill("pass123456");
  await page.getByRole("button", { name: "登录" }).click();
  await expect(page.getByText("累计收益")).toBeVisible();
});
```

- [ ] **Step 2: Run the end-to-end suite before the flow is complete**

Run: `cd frontend && npx playwright test ../e2e/tests/backtest-happy-path.spec.ts`
Expected: FAIL because the full workflow is not yet wired end to end

- [ ] **Step 3: Fill remaining gaps and document release verification**

```md
- Verify login works with the seeded demo user
- Verify one data source sync completes successfully
- Verify one backtest job reaches completed status
- Verify the results page shows metrics, curve, rebalances, and AI summary
```

- [ ] **Step 4: Re-run the end-to-end suite**

Run: `cd frontend && npx playwright test ../e2e/tests/backtest-happy-path.spec.ts`
Expected: PASS

- [ ] **Step 5: Commit release-readiness checks**

```bash
git add e2e docs/runbooks
git commit -m "test: add MVP release checks"
```

## Verification Matrix

Before claiming the MVP is complete, run the following commands and capture whether each one passed:

- `cd backend && pytest -v`
- `cd frontend && npm test -- --run`
- `cd frontend && npx playwright test ../e2e/tests`
- `bash scripts/dev/start.sh`

Expected outcome:

- Backend tests pass
- Frontend unit tests pass
- End-to-end tests pass
- Local startup script serves a usable app on the documented ports

## Open Execution Notes

- Use demo seed data early so UI and engine development can move in parallel
- Keep provider adapters behind a small interface so free and token sources can be swapped without touching the engine
- Do not introduce factor analysis, factor mining, arbitrary Python strategies, or multi-user SaaS concerns during MVP execution
- If SQLite performance becomes a blocker during development, profile first; do not switch databases mid-MVP without a measured reason

## Handoff

Plan complete and saved to `docs/superpowers/plans/2026-03-12-a-share-backtesting-mvp.md`. Ready to execute?

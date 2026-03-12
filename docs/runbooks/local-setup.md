# Local Setup

## Prerequisites

- Python 3.11+
- Node.js 20+
- npm 10+

## Backend

```bash
python3 -m venv backend/.venv
backend/.venv/bin/pip install -e 'backend[dev]'
```

## Frontend

```bash
cd frontend
npm install
npx playwright install chromium
```

## Start Both Services

```bash
bash scripts/dev/start.sh
```

Expected result:

- FastAPI serves `http://127.0.0.1:8000/api/health`
- Vite serves `http://127.0.0.1:5173/login`

## Smoke Test

```bash
cd frontend
npm run test:e2e -- ../e2e/tests/smoke-startup.spec.ts
```

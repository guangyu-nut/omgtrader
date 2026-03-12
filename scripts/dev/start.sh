#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
FRONTEND_DIR="$ROOT_DIR/frontend"

trap 'kill 0' EXIT INT TERM

if [ ! -x "$BACKEND_DIR/.venv/bin/python" ]; then
  echo "Missing backend virtualenv at $BACKEND_DIR/.venv" >&2
  exit 1
fi

(
  cd "$BACKEND_DIR"
  ./.venv/bin/alembic -c alembic.ini upgrade head
  PYTHONPATH="$BACKEND_DIR" ./.venv/bin/python "$ROOT_DIR/scripts/dev/seed_demo_data.py"
)

(
  cd "$BACKEND_DIR"
  ./.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
) &

(
  cd "$FRONTEND_DIR"
  npm run dev -- --host 127.0.0.1 --port 5173
) &

wait

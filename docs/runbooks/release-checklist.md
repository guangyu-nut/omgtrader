# Release Checklist

- Verify `bash scripts/dev/start.sh` runs migrations and seeds the demo environment without errors.
- Verify the demo user `demo / pass123456` can log in on `http://127.0.0.1:5173/login`.
- Verify `数据中心` shows seeded A 股覆盖范围 rows.
- Verify `策略中心` can create a stock pool and a Top N 等权轮动 strategy.
- Verify `回测中心` can launch a backtest with the latest strategy ID.
- Verify `结果页` shows `累计收益`、`最大回撤` 和 `策略总结`.

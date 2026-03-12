import { authStore } from "../stores/auth";

export type CurvePoint = {
  label: string;
  value: number;
};

export type RebalanceRow = {
  symbol: string;
  action: string;
};

export type BacktestResult = {
  metrics: {
    total_return: number | null;
    max_drawdown: number | null;
  };
  equity_curve: CurvePoint[];
  rebalances: RebalanceRow[];
};

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

export async function getBacktestResult(jobId: string): Promise<BacktestResult> {
  const response = await fetch(`${API_BASE_URL}/api/results/backtests/${jobId}`, {
    headers: authStore.token
      ? {
          Authorization: `Bearer ${authStore.token}`,
        }
      : undefined,
  });

  if (!response.ok) {
    throw new Error("加载回测结果失败");
  }

  return (await response.json()) as BacktestResult;
}

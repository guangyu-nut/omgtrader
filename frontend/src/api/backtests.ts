import { authStore } from "../stores/auth";

export type BacktestJobSummary = {
  id: string;
  status: string;
  metrics: {
    total_return: number | null;
    max_drawdown: number | null;
  };
};

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

export async function runBacktest(payload: { strategyInstanceId: string }): Promise<BacktestJobSummary> {
  const response = await fetch(`${API_BASE_URL}/api/backtests/jobs`, {
    body: JSON.stringify({
      strategy_instance_id: payload.strategyInstanceId,
    }),
    headers: {
      Authorization: `Bearer ${authStore.token}`,
      "Content-Type": "application/json",
    },
    method: "POST",
  });

  if (!response.ok) {
    throw new Error("启动回测失败");
  }

  return (await response.json()) as BacktestJobSummary;
}

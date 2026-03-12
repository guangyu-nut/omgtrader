import { authStore } from "../stores/auth";

export type StockPool = {
  id: string;
  name: string;
  input_mode: string;
  symbols: string[];
};

export type StrategyInstance = {
  id: string;
  name: string;
  template_type: string;
  stock_pool_id: string;
  ranking_metric: string;
  hold_count: number;
  rebalance_frequency: string;
  slippage_bps: number;
  commission_bps: number;
  benchmark_symbol: string;
};

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

function buildHeaders() {
  return authStore.token
    ? {
        Authorization: `Bearer ${authStore.token}`,
        "Content-Type": "application/json",
      }
    : {
        "Content-Type": "application/json",
      };
}

export async function createStockPool(payload: {
  name: string;
  input_mode: "manual";
  symbols: string[];
}): Promise<StockPool> {
  const response = await fetch(`${API_BASE_URL}/api/strategies/stock-pools`, {
    body: JSON.stringify(payload),
    headers: buildHeaders(),
    method: "POST",
  });

  if (!response.ok) {
    throw new Error("创建股票池失败");
  }

  return (await response.json()) as StockPool;
}

export async function createStrategy(payload: {
  name: string;
  template_type: "top_n_equal_weight";
  stock_pool_id: string;
  ranking_metric: string;
  hold_count: number;
  rebalance_frequency: "daily";
  slippage_bps: number;
  commission_bps: number;
  benchmark_symbol: string;
}): Promise<StrategyInstance> {
  const response = await fetch(`${API_BASE_URL}/api/strategies/strategy-instances`, {
    body: JSON.stringify(payload),
    headers: buildHeaders(),
    method: "POST",
  });

  if (!response.ok) {
    throw new Error("创建策略失败");
  }

  return (await response.json()) as StrategyInstance;
}

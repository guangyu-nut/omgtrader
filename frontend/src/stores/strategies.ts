import { reactive } from "vue";

import {
  createStockPool,
  createStrategy,
  type StockPool,
  type StrategyInstance,
} from "../api/strategies";

type StrategiesState = {
  currentStockPoolId: string;
  latestStrategyId: string;
  stockPools: StockPool[];
  strategies: StrategyInstance[];
};

function getStorage() {
  if (typeof window === "undefined") {
    return null;
  }

  const storage = window.localStorage;
  return storage && typeof storage.getItem === "function" ? storage : null;
}

const storage = getStorage();
const initialStockPoolId = storage?.getItem("lastStockPoolId") ?? "";
const initialStrategyId = storage?.getItem("lastStrategyId") ?? "";

const state = reactive<StrategiesState>({
  currentStockPoolId: initialStockPoolId,
  latestStrategyId: initialStrategyId,
  stockPools: [],
  strategies: [],
});

export const strategyStore = {
  get currentStockPoolId() {
    return state.currentStockPoolId;
  },
  get latestStrategyId() {
    return state.latestStrategyId;
  },
  get strategies() {
    return state.strategies;
  },
  async createStockPool(payload: { name: string; symbols: string[] }) {
    const stockPool = await createStockPool({
      input_mode: "manual",
      name: payload.name,
      symbols: payload.symbols,
    });

    state.currentStockPoolId = stockPool.id;
    state.stockPools.unshift(stockPool);
    storage?.setItem("lastStockPoolId", stockPool.id);
    return stockPool;
  },
  async createStrategy(payload: {
    name: string;
    hold_count: number;
    slippage_bps: number;
    commission_bps: number;
    benchmark_symbol: string;
  }) {
    if (!state.currentStockPoolId) {
      throw new Error("请先创建股票池");
    }

    const strategy = await createStrategy({
      benchmark_symbol: payload.benchmark_symbol,
      commission_bps: payload.commission_bps,
      hold_count: payload.hold_count,
      name: payload.name,
      ranking_metric: "close",
      rebalance_frequency: "daily",
      slippage_bps: payload.slippage_bps,
      stock_pool_id: state.currentStockPoolId,
      template_type: "top_n_equal_weight",
    });

    state.latestStrategyId = strategy.id;
    state.strategies.unshift(strategy);
    storage?.setItem("lastStrategyId", strategy.id);
    return strategy;
  },
  reset() {
    state.currentStockPoolId = "";
    state.latestStrategyId = "";
    state.stockPools = [];
    state.strategies = [];
    storage?.removeItem("lastStockPoolId");
    storage?.removeItem("lastStrategyId");
  },
};

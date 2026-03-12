import { reactive } from "vue";

import { runBacktest, type BacktestJobSummary } from "../api/backtests";

type BacktestsState = {
  recentJobs: BacktestJobSummary[];
};

const state = reactive<BacktestsState>({
  recentJobs: [],
});

export const backtestStore = {
  get recentJobs() {
    return state.recentJobs;
  },
  async loadRecentJobs() {
    return state.recentJobs;
  },
  async runJob(payload: { strategyInstanceId: string }) {
    const job = await runBacktest(payload);
    state.recentJobs.unshift(job);
    return job;
  },
  reset() {
    state.recentJobs = [];
  },
};

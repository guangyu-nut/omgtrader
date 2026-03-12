import { reactive } from "vue";

import {
  createDataSource,
  getCoverageRows,
  getSyncTasks,
  type CoverageRow,
  type DataSource,
  type SyncTask,
} from "../api/marketData";

type MarketDataState = {
  coverages: CoverageRow[];
  dataSources: DataSource[];
  syncTasks: SyncTask[];
};

const state = reactive<MarketDataState>({
  coverages: [],
  dataSources: [],
  syncTasks: [],
});

export const marketDataStore = {
  get coverages() {
    return state.coverages;
  },
  get dataSources() {
    return state.dataSources;
  },
  get syncTasks() {
    return state.syncTasks;
  },
  async createDataSource(payload: { name: string; provider_type: string; enabled: boolean }) {
    const dataSource = await createDataSource(payload);
    state.dataSources.unshift(dataSource);
    return dataSource;
  },
  async loadCoverage() {
    state.coverages = await getCoverageRows();
    return state.coverages;
  },
  async loadDataSources() {
    return state.dataSources;
  },
  async loadSyncTasks() {
    state.syncTasks = await getSyncTasks();
    return state.syncTasks;
  },
  reset() {
    state.coverages = [];
    state.dataSources = [];
    state.syncTasks = [];
  },
};

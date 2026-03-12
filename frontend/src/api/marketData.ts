import { authStore } from "../stores/auth";

export type DataSource = {
  id: string;
  name: string;
  provider_type: string;
  enabled: boolean;
};

export type SyncTask = {
  id: string;
  data_source_config_id: string;
  status: string;
  started_at: string | null;
  finished_at: string | null;
};

export type CoverageRow = {
  symbol_code: string;
  daily_start: string | null;
  daily_end: string | null;
  minute_start: string | null;
  minute_end: string | null;
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

export async function createDataSource(payload: {
  name: string;
  provider_type: string;
  enabled: boolean;
}): Promise<DataSource> {
  const response = await fetch(`${API_BASE_URL}/api/market-data/data-sources`, {
    body: JSON.stringify(payload),
    headers: buildHeaders(),
    method: "POST",
  });

  if (!response.ok) {
    throw new Error("创建数据源失败");
  }

  return (await response.json()) as DataSource;
}

export async function getSyncTasks(): Promise<SyncTask[]> {
  const response = await fetch(`${API_BASE_URL}/api/market-data/sync-tasks`, {
    headers: buildHeaders(),
  });

  if (!response.ok) {
    throw new Error("加载同步任务失败");
  }

  return (await response.json()) as SyncTask[];
}

export async function getCoverageRows(): Promise<CoverageRow[]> {
  const response = await fetch(`${API_BASE_URL}/api/market-data/coverage`, {
    headers: buildHeaders(),
  });

  if (!response.ok) {
    throw new Error("加载覆盖范围失败");
  }

  return (await response.json()) as CoverageRow[];
}

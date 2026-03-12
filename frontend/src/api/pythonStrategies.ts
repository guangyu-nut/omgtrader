import { authStore } from "../stores/auth";


export type PythonStrategyListItem = {
  id: string;
  name: string;
  description: string;
  tags: string[];
  updated_at: string;
};

export type PythonStrategyDetail = PythonStrategyListItem & {
  parameter_schema_text: string;
  code: string;
  created_at: string;
};

export type PythonStrategyPayload = {
  name: string;
  description: string;
  tags: string[];
  parameter_schema_text: string;
  code: string;
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

async function parseJson<T>(response: Response, message: string): Promise<T> {
  if (!response.ok) {
    throw new Error(message);
  }

  return (await response.json()) as T;
}

export async function listPythonStrategies(): Promise<PythonStrategyListItem[]> {
  const response = await fetch(`${API_BASE_URL}/api/strategies/python`, {
    headers: buildHeaders(),
  });

  return parseJson<PythonStrategyListItem[]>(response, "加载 Python 策略失败");
}

export async function getPythonStrategy(strategyId: string): Promise<PythonStrategyDetail> {
  const response = await fetch(`${API_BASE_URL}/api/strategies/python/${strategyId}`, {
    headers: buildHeaders(),
  });

  return parseJson<PythonStrategyDetail>(response, "加载 Python 策略详情失败");
}

export async function createPythonStrategy(payload: PythonStrategyPayload): Promise<PythonStrategyDetail> {
  const response = await fetch(`${API_BASE_URL}/api/strategies/python`, {
    body: JSON.stringify(payload),
    headers: buildHeaders(),
    method: "POST",
  });

  return parseJson<PythonStrategyDetail>(response, "创建 Python 策略失败");
}

export async function updatePythonStrategy(
  strategyId: string,
  payload: PythonStrategyPayload,
): Promise<PythonStrategyDetail> {
  const response = await fetch(`${API_BASE_URL}/api/strategies/python/${strategyId}`, {
    body: JSON.stringify(payload),
    headers: buildHeaders(),
    method: "PUT",
  });

  return parseJson<PythonStrategyDetail>(response, "更新 Python 策略失败");
}

export async function deletePythonStrategy(strategyId: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/api/strategies/python/${strategyId}`, {
    headers: buildHeaders(),
    method: "DELETE",
  });

  if (!response.ok) {
    throw new Error("删除 Python 策略失败");
  }
}

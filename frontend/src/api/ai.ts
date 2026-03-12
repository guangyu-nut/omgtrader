import { authStore } from "../stores/auth";

export type AiInsight = {
  summary: string;
  risks: string[];
};

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

export async function generateInsight(jobId: string): Promise<AiInsight> {
  const response = await fetch(`${API_BASE_URL}/api/ai/backtests/${jobId}/insights`, {
    headers: authStore.token
      ? {
          Authorization: `Bearer ${authStore.token}`,
        }
      : undefined,
    method: "POST",
  });

  if (!response.ok) {
    throw new Error("生成 AI 解读失败");
  }

  return (await response.json()) as AiInsight;
}

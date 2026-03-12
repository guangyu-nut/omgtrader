export type LoginPayload = {
  username: string;
  password: string;
};

export type LoginResponse = {
  token: string;
};

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

export async function login(payload: LoginPayload): Promise<LoginResponse> {
  const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
    body: JSON.stringify(payload),
    headers: {
      "Content-Type": "application/json",
    },
    method: "POST",
  });

  if (!response.ok) {
    throw new Error("登录失败");
  }

  return (await response.json()) as LoginResponse;
}

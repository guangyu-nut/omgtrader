import { reactive } from "vue";

import { login, type LoginPayload } from "../api/auth";

type AuthState = {
  token: string | null;
};

function getStorage() {
  if (typeof window === "undefined") {
    return null;
  }

  const storage = window.localStorage;
  return storage && typeof storage.getItem === "function" ? storage : null;
}

const storage = getStorage();
const state = reactive<AuthState>({
  token: storage?.getItem("authToken") ?? null,
});

export const authStore = {
  get token() {
    return state.token;
  },
  async login(payload: LoginPayload) {
    const response = await login(payload);
    state.token = response.token;
    storage?.setItem("authToken", response.token);
    return response;
  },
  reset() {
    state.token = null;
    storage?.removeItem("authToken");
  },
};

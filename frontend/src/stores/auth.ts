import { reactive } from "vue";

import { login, type LoginPayload } from "../api/auth";

type AuthState = {
  token: string | null;
};

const state = reactive<AuthState>({
  token: null,
});

export const authStore = {
  get token() {
    return state.token;
  },
  async login(payload: LoginPayload) {
    const response = await login(payload);
    state.token = response.token;
    return response;
  },
  reset() {
    state.token = null;
  },
};

import { flushPromises, mount } from "@vue/test-utils";
import { beforeEach, describe, expect, it, vi } from "vitest";

import * as authApi from "../api/auth";
import { router } from "../router";
import { authStore } from "../stores/auth";
import LoginView from "../views/LoginView.vue";

describe("LoginView", () => {
  beforeEach(async () => {
    authStore.reset();
    await router.push("/login");
    await router.isReady();
    vi.restoreAllMocks();
  });

  it("submits credentials and stores the session", async () => {
    vi.spyOn(authApi, "login").mockResolvedValue({ token: "session-token" });

    const wrapper = mount(LoginView, {
      global: {
        plugins: [router],
      },
    });

    await wrapper.get("#username").setValue("demo");
    await wrapper.get("#password").setValue("pass123456");
    await wrapper.get("form").trigger("submit.prevent");
    await flushPromises();

    expect(authStore.token).toBe("session-token");
  });

  it("renders the trading desk login copy", () => {
    const wrapper = mount(LoginView, {
      global: {
        plugins: [router],
      },
    });

    expect(wrapper.text()).toContain("A 股量化研究终端");
    expect(wrapper.text()).toContain("本地运行");
  });
});

import { flushPromises, mount } from "@vue/test-utils";
import { beforeEach, describe, expect, it } from "vitest";

import App from "../App.vue";
import { router } from "../router";

describe("App shell", () => {
  beforeEach(async () => {
    await router.push("/login");
    await router.isReady();
  });

  it("hides the sidebar on login", async () => {
    const wrapper = mount(App, {
      global: {
        plugins: [router],
      },
    });

    await flushPromises();

    expect(wrapper.find('[data-testid="app-sidebar"]').exists()).toBe(false);
  });

  it("shows the sidebar on shell routes", async () => {
    await router.push("/workbench");

    const wrapper = mount(App, {
      global: {
        plugins: [router],
      },
    });

    await flushPromises();

    expect(wrapper.get('[data-testid="app-sidebar"]').text()).toContain("工作台");
    expect(wrapper.get('[data-testid="app-sidebar"]').text()).toContain("数据中心");
    expect(wrapper.get('[data-testid="app-sidebar"]').text()).toContain("策略中心");
    expect(wrapper.get('[data-testid="app-sidebar"]').text()).toContain("回测中心");
  });

  it("marks the active navigation item", async () => {
    await router.push("/strategy-center");

    const wrapper = mount(App, {
      global: {
        plugins: [router],
      },
    });

    await flushPromises();

    expect(wrapper.get('[data-route-name="strategy-center"]').classes()).toContain("is-active");
  });
});

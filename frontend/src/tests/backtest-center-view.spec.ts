import { mount } from "@vue/test-utils";
import { describe, expect, it } from "vitest";

import BacktestCenterView from "../views/BacktestCenterView.vue";

describe("BacktestCenterView", () => {
  it("shows the backtest launch desk", () => {
    const wrapper = mount(BacktestCenterView);

    expect(wrapper.text()).toContain("任务发射台");
    expect(wrapper.text()).toContain("回测任务");
    expect(wrapper.text()).toContain("开始回测");
  });
});

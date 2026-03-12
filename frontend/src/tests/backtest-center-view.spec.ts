import { mount } from "@vue/test-utils";
import { describe, expect, it } from "vitest";

import BacktestCenterView from "../views/BacktestCenterView.vue";

describe("BacktestCenterView", () => {
  it("launches a backtest job from the backtest center", () => {
    const wrapper = mount(BacktestCenterView);

    expect(wrapper.text()).toContain("开始回测");
  });
});

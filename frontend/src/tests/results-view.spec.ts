import { flushPromises, mount } from "@vue/test-utils";
import { beforeEach, describe, expect, it, vi } from "vitest";

import * as aiApi from "../api/ai";
import * as resultsApi from "../api/results";
import { router } from "../router";
import ResultsView from "../views/ResultsView.vue";

describe("ResultsView", () => {
  beforeEach(async () => {
    vi.restoreAllMocks();
    await router.push("/results/job-1");
    await router.isReady();
  });

  it("renders metrics and equity curve data", async () => {
    vi.spyOn(resultsApi, "getBacktestResult").mockResolvedValue({
      equity_curve: [
        { label: "起点", value: 1 },
        { label: "终点", value: 1.05 },
      ],
      metrics: {
        max_drawdown: 0.02,
        total_return: 0.05,
      },
      rebalances: [],
    });
    vi.spyOn(aiApi, "generateInsight").mockResolvedValue({
      summary: "回测表现稳健",
      risks: ["换手较高"],
    });

    const wrapper = mount(ResultsView, {
      global: {
        plugins: [router],
      },
    });

    await flushPromises();

    expect(wrapper.text()).toContain("分析总览");
    expect(wrapper.text()).toContain("最大回撤");
    expect(wrapper.text()).toContain("累计收益");
    expect(wrapper.text()).toContain("策略总结");
  });
});

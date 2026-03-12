import { flushPromises, mount } from "@vue/test-utils";
import { beforeEach, describe, expect, it, vi } from "vitest";

import * as aiApi from "../api/ai";
import AiInsightPanel from "../components/results/AiInsightPanel.vue";

describe("AiInsightPanel", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it("shows generated insight content", async () => {
    vi.spyOn(aiApi, "generateInsight").mockResolvedValue({
      risks: ["回撤控制还可以更稳"],
      summary: "策略总结",
    });

    const wrapper = mount(AiInsightPanel, {
      props: {
        jobId: "job-1",
      },
    });

    await flushPromises();

    expect(wrapper.text()).toContain("策略总结");
  });
});

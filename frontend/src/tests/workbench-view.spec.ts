import { mount } from "@vue/test-utils";
import { describe, expect, it } from "vitest";

import WorkbenchView from "../views/WorkbenchView.vue";

describe("WorkbenchView", () => {
  it("shows recent backtest summaries on the workbench", () => {
    const wrapper = mount(WorkbenchView);

    expect(wrapper.text()).toContain("最近回测");
  });
});

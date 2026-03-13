import { mount } from "@vue/test-utils";
import { describe, expect, it } from "vitest";

import WorkbenchView from "../views/WorkbenchView.vue";

describe("WorkbenchView", () => {
  it("shows the workbench overview cards", () => {
    const wrapper = mount(WorkbenchView);

    expect(wrapper.text()).toContain("研究总览");
    expect(wrapper.text()).toContain("最近回测");
  });
});

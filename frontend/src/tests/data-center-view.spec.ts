import { mount } from "@vue/test-utils";
import { describe, expect, it } from "vitest";

import DataCenterView from "../views/DataCenterView.vue";

describe("DataCenterView", () => {
  it("shows the data operations sections", () => {
    const wrapper = mount(DataCenterView);

    expect(wrapper.text()).toContain("数据运行面板");
    expect(wrapper.text()).toContain("覆盖范围");
    expect(wrapper.text()).toContain("最近更新时间");
  });
});

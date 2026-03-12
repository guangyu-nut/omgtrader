import { mount } from "@vue/test-utils";
import { describe, expect, it } from "vitest";

import DataCenterView from "../views/DataCenterView.vue";

describe("DataCenterView", () => {
  it("shows data source status rows", () => {
    const wrapper = mount(DataCenterView);

    expect(wrapper.text()).toContain("最近更新时间");
  });
});
